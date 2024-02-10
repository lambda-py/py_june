variable "aws_region" {
  description = "The AWS region to create resources in."
  type        = string
  default     = "eu-west-3"
}

variable "instance_type" {
  description = "The instance type of the EC2 instance."
  type        = string
  default     = "t2.micro"
}

variable "ubuntu_yammy_ami" {
  description = "The AMI ID for the EC2 instance."
  type        = string
  default     = "ami-0b72d6fdeb8505311"
}

variable "db_instance_type" {
  description = "The instance type of the RDS instance."
  type        = string
  default     = "db.t2.micro"
}

variable "db_name" {
  description = "The name of the database to create."
  type        = string
}

variable "db_user" {
  description = "The username for the database."
  type        = string
}

variable "db_password" {
  description = "The password for the database user."
  type        = string
}
