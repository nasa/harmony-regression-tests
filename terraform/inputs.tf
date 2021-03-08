variable "aws_region" {
  description = "AWS region to create resources in"
  default     = "us-west-2"
}

variable "instance_type" {
  description = "EC2 instance type for the regression test runner"
  default     = "t2.xlarge"
}

variable "key_name" {
  description = "Key pair name to use for the harmony regression test instance."
  default     = "bamboo"
}

variable "environment_name" {
  description = "environment name, e.g. sit, uat, prod, harmony-35, etc"
}

