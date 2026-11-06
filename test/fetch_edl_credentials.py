"""Assume the ETQTest-harmony-regression role and fetch EDL credentials from SSM.

Prints `export EDL_USER=...` / `export EDL_PASSWORD=...` lines so build-netrc.sh
can `source` this script's output without the credentials ever touching ASTRA's
plaintext test configuration.
"""

import os
import shlex
import sys

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def main() -> None:
    role_arn = os.getenv("EDL_SECRETS_ROLE_ARN")
    if not role_arn:
        print(
            "EDL_SECRETS_ROLE_ARN is not set; skipping SSM credential fetch.",
            file=sys.stderr,
        )
        return

    try:
        sts = boto3.client("sts")
        assumed = sts.assume_role(
            RoleArn=role_arn, RoleSessionName="harmony-regression"
        )["Credentials"]

        ssm = boto3.client(
            "ssm",
            aws_access_key_id=assumed["AccessKeyId"],
            aws_secret_access_key=assumed["SecretAccessKey"],
            aws_session_token=assumed["SessionToken"],
        )

        user = ssm.get_parameter(
            Name="/astra/harmony-regression-tests/EDL_USER", WithDecryption=True
        )["Parameter"]["Value"]
        password = ssm.get_parameter(
            Name="/astra/harmony-regression-tests/EDL_PASSWORD", WithDecryption=True
        )["Parameter"]["Value"]
    except (ClientError, BotoCoreError) as error:
        print(
            f"Failed to fetch EDL credentials from SSM via role {role_arn}: {error}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"export EDL_USER={shlex.quote(user)}")
    print(f"export EDL_PASSWORD={shlex.quote(password)}")


if __name__ == "__main__":
    main()
