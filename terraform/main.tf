terraform {
  required_version = ">= 0.12"
}

provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "harmony-regression-test" {
  ami                  = data.aws_ami.ngap.id
  subnet_id            = tolist(data.aws_subnet_ids.app.ids)[0]
  instance_type        = var.instance_type
  iam_instance_profile = aws_iam_instance_profile.harmony_instance_profile.name
  key_name             = var.key_name
  count                = 1

  # user_data = templatefile("${path.module}/harmony-user-data.tmpl", {
  #   environment_name = var.environment_name
  #   ssh_keys_bucket  = aws_s3_bucket.authorized_keys.id
  #   }
  # )

  vpc_security_group_ids = [aws_security_group.harmony_instances.id]
  tags = {
    Name = "harmony-regression-test-${var.environment_name}"
  }

  provisioner "file" {
    # TODO move main directory contents to subdir to avoid copying terraform files
    source      = ".."
    destination = "/home/ec2-user"
  }

  lifecycle {
    create_before_destroy = true
    ignore_changes        = [tags] # Prevents us clobbering NGAP-created tags
  }
}