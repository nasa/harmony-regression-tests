terraform {
  required_version = ">= 0.12"
}

provider "aws" {
  region = var.aws_region
}

resource "aws_security_group" "harmony_regression_test" {
  name        = "harmony-regression-test-sg-${var.environment_name}"
  description = "Allow SSH and harmony endpoint traffic for ${var.environment_name}"
  vpc_id      = data.aws_vpc.app.id

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"
    cidr_blocks = [
      data.aws_vpc.app.cidr_block_associations[0].cidr_block
    ]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "harmony-regression-test-${var.environment_name}"
  }

  lifecycle {
    ignore_changes = [description]
  }
}

resource "aws_instance" "harmony_regression_test" {
  ami                  = data.aws_ami.ngap.id
  subnet_id            = tolist(data.aws_subnet_ids.app.ids)[0]
  instance_type        = var.instance_type
  iam_instance_profile = data.aws_iam_instance_profile.regression_test_instance_profile.name
  key_name             = var.key_name

  user_data = file("${path.module}/harmony-user-data.tmpl")

  vpc_security_group_ids = [aws_security_group.harmony_regression_test.id]
  tags = {
    Name = "harmony-regression-test-${var.environment_name}"
  }

  lifecycle {
    create_before_destroy = true
    ignore_changes        = [tags] # Prevents us clobbering NGAP-created tags
  }
}