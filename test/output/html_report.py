import nbformat
from nbconvert import HTMLExporter

# Generate HTML report
exporter = HTMLExporter()
html_report = exporter.from_notebook_node(nbformat.read('harmony/Results.ipynb', as_version=4))
with open('report.html', 'w') as f:
    f.write(html_report[0])
