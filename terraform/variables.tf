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

variable "ubuntu_focal_ami" {
  description = "The AMI ID for the EC2 instance."
  type        = string
  default     = "ami-08d0e3f9e0d3a5fb1"
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

variable "db_username" {
  description = "The username for the database."
  type        = string
}

variable "db_password" {
  description = "The password for the database user."
  type        = string
}

# The CIDR block for the VPC
variable "vpc_cidr" {
  description = "The CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

# The CIDR blocks for the public subnets. This is a list in case you want
# to define multiple public subnets.
variable "private_subnet_cidrs" {
  description = "A list of CIDR blocks for the public subnets."
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

# The availability zones in which to place the subnets. This list should align
# with the 'public_subnet_cidrs' list in length and order.
variable "availability_zones" {
  description = "A list of availability zones in which to create subnets."
  type        = list(string)
  default     = ["eu-west-3a", "eu-west-3b"]
}

# CIDR blocks allowed for SSH access to instances within the security group.
# Adjust this according to your security requirements.
# TODO change to server ip. Open to the world; it's recommended to be more restrictive
variable "allowed_ssh_cidr" {
  description = "CIDR blocks allowed to SSH to the instances. Be restrictive here for security."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "key_name" {
  description = "The name of the key pair to use for the instance."
  type        = string
}
