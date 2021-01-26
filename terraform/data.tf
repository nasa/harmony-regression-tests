data "aws_caller_identity" "current" {
}

data "aws_canonical_user_id" "current_user" {}

data "aws_region" "current" {
}

data "aws_vpc" "app" {
  filter {
    name   = "tag:Name"
    values = ["Application VPC"]
  }
}

data "aws_subnet_ids" "app" {
  vpc_id = data.aws_vpc.app.id

  tags = {
    Name = "Private application *"
  }
}

data "aws_ami" "ngap" {
  most_recent = true

  filter {
    name   = "name"
    values = ["edc-app-base-*-amzn-linux2-x86_64"]
  }

  owners = ["863143145967", "182918467801"]
}

data "aws_iam_instance_profile" "regression_test_instance_profile" {
  name = "harmony-${var.environment_name}-instance-profile"
}