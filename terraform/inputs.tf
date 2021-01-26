variable "aws_region" {
  description = "AWS region to create resources in"
  default     = "us-west-2"
}

variable "instance_type" {
  description = "EC2 instance type for the harmony application"
  default     = "t2.medium"
}

variable "key_name" {
  description = "Key pair name to use for the harmony EC2 instance."
}

variable "environment_name" {
  description = "environment name, e.g. sit, uat, prod, harmony-35, etc"
}
