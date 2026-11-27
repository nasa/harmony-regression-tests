"""Generate per-test results from a papermill-executed regression notebook.

Each code cell tagged ``test`` in the notebook is treated as an individual test.
Test cells should also be tagged ``raises-exception`` so that a failing test
does not stop papermill from executing the remaining tests. The test name is
taken from the nearest preceding markdown heading.

A test is:

* failed - if the cell produced an error output.
* skipped - if the cell completed without error, but printed a message
  indicating that the test is skipped or not configured for the environment.
* not run - if the cell was never executed, e.g., due to a setup cell failure.
* passed - otherwise.

Untagged cells are treated as setup. If one of them fails, an extra failed
test is reported for it. Notebooks without any ``test`` tagged cells are
reported as a single test, which preserves the previous whole-notebook result.

Outputs written to the specified output directory:

* test_results.json - results consumed by report.py for ASTRA submission.
* junit.xml - JUnit XML report.
* summary.md - Markdown summary, e.g., for a GitHub Actions step summary.

Usage:
    python3 notebook_report.py <Results.ipynb> <suite name> <output directory> \
        [--notebook-name <source notebook>] [--notebook-status passed|failed]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from xml.etree.ElementTree import Element, ElementTree, SubElement, indent

TEST_TAG = 'test'
PAPERMILL_ERROR_TAG = 'papermill-error-cell-tag'
SKIP_PATTERN = re.compile(r'\bskip|not configured', re.IGNORECASE)
ANSI_PATTERN = re.compile(r'\x1b\[[0-9;]*[A-Za-z]')
# Characters that are not permitted in XML 1.0 documents.
INVALID_XML_PATTERN = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')

PASSED = 'passed'
FAILED = 'failed'
SKIPPED = 'skipped'
NOT_RUN = 'not run'


def clean_text(text: str) -> str:
    """Remove ANSI colour codes and characters that are invalid in XML."""
    return INVALID_XML_PATTERN.sub('', ANSI_PATTERN.sub('', text))


def join_text(text: str | list[str]) -> str:
    """Notebook JSON may store multi-line text as a list of strings."""
    return ''.join(text) if isinstance(text, list) else text


def get_source(cell: dict) -> str:
    return join_text(cell.get('source', ''))


def get_tags(cell: dict) -> list[str]:
    return cell.get('metadata', {}).get('tags', [])


def get_heading(cell: dict) -> str | None:
    """Return the first markdown heading in a cell, if there is one."""
    for line in get_source(cell).splitlines():
        if line.startswith('#'):
            heading = re.sub(r'<[^>]+>', '', line.lstrip('#'))
            heading = heading.replace('`', '').replace('**', '').strip()
            return heading.rstrip(':.').strip() or None
    return None


def get_cell_result(cell: dict) -> dict:
    """Determine the status of a single code cell from papermill metadata."""
    papermill_metadata = cell.get('metadata', {}).get('papermill', {})
    outputs = cell.get('outputs', [])
    errors = [output for output in outputs if output.get('output_type') == 'error']
    stream_text = ''.join(
        join_text(output.get('text', ''))
        for output in outputs
        if output.get('output_type') == 'stream'
    )

    result = {
        'duration': papermill_metadata.get('duration') or 0,
        'message': '',
        'details': '',
    }

    if errors:
        result['status'] = FAILED
        result['message'] = clean_text(f'{errors[0]["ename"]}: {errors[0]["evalue"]}')
        result['details'] = clean_text('\n'.join(errors[0].get('traceback', [])))
    elif papermill_metadata.get('exception') is True:
        result['status'] = FAILED
        result['message'] = 'Cell execution failed without an error output.'
    elif papermill_metadata.get('status') != 'completed':
        result['status'] = NOT_RUN
        result['message'] = 'Not run: notebook execution stopped before this test.'
    elif SKIP_PATTERN.search(stream_text):
        result['status'] = SKIPPED
        result['message'] = clean_text(stream_text.strip().splitlines()[-1])
    else:
        result['status'] = PASSED

    result['output'] = clean_text(stream_text)
    return result


def collect_results(notebook: dict, notebook_name: str) -> list[dict]:
    """Return a list of test results for the executed notebook."""
    results = []
    test_cells_found = False
    heading = None
    titles_seen = {}

    for index, cell in enumerate(notebook.get('cells', [])):
        if PAPERMILL_ERROR_TAG in get_tags(cell):
            continue

        if cell.get('cell_type') == 'markdown':
            heading = get_heading(cell) or heading
            continue

        if cell.get('cell_type') != 'code':
            continue

        is_test = TEST_TAG in get_tags(cell)
        test_cells_found = test_cells_found or is_test
        result = get_cell_result(cell)

        if not is_test and result['status'] != FAILED:
            continue

        title = heading or f'Cell {index}'
        if not is_test:
            title = f'Setup: {title} (cell {index})'

        # Ensure test titles are unique within the suite.
        titles_seen[title] = titles_seen.get(title, 0) + 1
        if titles_seen[title] > 1:
            title = f'{title} ({titles_seen[title]})'

        results.append({'title': title, 'cell_index': index, **result})

    if not test_cells_found:
        # Report the whole notebook as a single test, retaining any failure.
        failures = [result for result in results if result['status'] == FAILED]
        results = [
            {
                'title': notebook_name,
                'cell_index': None,
                'status': FAILED if failures else PASSED,
                'duration': notebook.get('metadata', {})
                .get('papermill', {})
                .get('duration')
                or 0,
                'message': failures[0]['message'] if failures else '',
                'details': failures[0]['details'] if failures else '',
                'output': '',
            }
        ]

    return results


def reconcile_with_notebook_status(
    results: list[dict], notebook_status: str | None
) -> list[dict]:
    """Ensure the report agrees with the overall papermill exit status.

    For example, a kernel crash or timeout may not leave an error output in the
    notebook, but papermill will still have exited with a failure.
    """
    if notebook_status == FAILED and not any(
        result['status'] == FAILED for result in results
    ):
        results.append(
            {
                'title': 'Notebook execution',
                'cell_index': None,
                'status': FAILED,
                'duration': 0,
                'message': 'papermill exited with a failure status.',
                'details': '',
                'output': '',
            }
        )
    return results


def count_statuses(results: list[dict]) -> dict:
    counts = {status: 0 for status in (PASSED, FAILED, SKIPPED, NOT_RUN)}
    for result in results:
        counts[result['status']] += 1
    return counts


def write_junit(results: list[dict], suite_name: str, output_path: Path) -> None:
    counts = count_statuses(results)
    total_time = sum(result['duration'] for result in results)
    attributes = {
        'name': suite_name,
        'tests': str(len(results)),
        'failures': str(counts[FAILED]),
        'errors': '0',
        'skipped': str(counts[SKIPPED] + counts[NOT_RUN]),
        'time': f'{total_time:.3f}',
    }

    test_suites = Element('testsuites', attributes)
    test_suite = SubElement(test_suites, 'testsuite', attributes)

    for result in results:
        test_case = SubElement(
            test_suite,
            'testcase',
            {
                'classname': suite_name,
                'name': result['title'],
                'time': f'{result["duration"]:.3f}',
            },
        )
        if result['status'] == FAILED:
            failure = SubElement(test_case, 'failure', {'message': result['message']})
            failure.text = result['details']
        elif result['status'] in (SKIPPED, NOT_RUN):
            SubElement(test_case, 'skipped', {'message': result['message']})

        if result['output']:
            system_out = SubElement(test_case, 'system-out')
            system_out.text = result['output']

    indent(test_suites)
    ElementTree(test_suites).write(output_path, encoding='utf-8', xml_declaration=True)


def format_counts(counts: dict) -> str:
    return ', '.join(f'{count} {status}' for status, count in counts.items() if count)


def write_markdown(results: list[dict], suite_name: str, output_path: Path) -> None:
    icons = {PASSED: '✅', FAILED: '❌', SKIPPED: '⏭️', NOT_RUN: '⏸️'}
    lines = [
        f'### {suite_name}: {format_counts(count_statuses(results))}',
        '',
        '| Status | Test | Duration (s) | Message |',
        '| --- | --- | --- | --- |',
    ]
    for result in results:
        message = result['message'].replace('|', '\\|').replace('\n', ' ')
        lines.append(
            f'| {icons[result["status"]]} {result["status"]} | {result["title"]} '
            f'| {result["duration"]:.1f} | {message} |'
        )
    output_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def print_summary(results: list[dict], suite_name: str) -> None:
    print(f'\n{suite_name} test results: {format_counts(count_statuses(results))}')
    for result in results:
        line = f'  {result["status"].upper():8} {result["title"]}'
        if result['status'] != PASSED and result['message']:
            line += f' - {result["message"]}'
        print(line)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('notebook', type=Path, help='Executed papermill notebook.')
    parser.add_argument('suite_name', help='Name of the regression test suite.')
    parser.add_argument('output_dir', type=Path, help='Directory for report files.')
    parser.add_argument(
        '--notebook-name',
        help='Source notebook name, used as the test title for untagged notebooks.',
    )
    parser.add_argument(
        '--notebook-status',
        choices=[PASSED, FAILED],
        help='Overall papermill result, used to reconcile the per-test results.',
    )
    args = parser.parse_args()

    if args.notebook.exists():
        notebook = json.loads(args.notebook.read_text(encoding='utf-8'))
        results = collect_results(notebook, args.notebook_name or args.notebook.name)
    else:
        results = [
            {
                'title': args.suite_name,
                'cell_index': None,
                'status': FAILED,
                'duration': 0,
                'message': f'Executed notebook not found: {args.notebook}',
                'details': '',
                'output': '',
            }
        ]

    results = reconcile_with_notebook_status(results, args.notebook_status)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'test_results.json').write_text(
        json.dumps({'suite': args.suite_name, 'tests': results}, indent=2),
        encoding='utf-8',
    )
    write_junit(results, args.suite_name, args.output_dir / 'junit.xml')
    write_markdown(results, args.suite_name, args.output_dir / 'summary.md')
    print_summary(results, args.suite_name)


if __name__ == '__main__':
    try:
        main()
    except Exception as exception:  # Reporting must not mask the test result.
        print(f'Failed to generate test report: {exception}', file=sys.stderr)
        sys.exit(1)
