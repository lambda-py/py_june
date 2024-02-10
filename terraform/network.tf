# Define the VPC
resource "aws_vpc" "django_vpc" {
  cidr_block = var.vpc_cidr
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "DjangoVPC"
  }
}

# Create an Internet Gateway for the VPC
resource "aws_internet_gateway" "django_igw" {
  vpc_id = aws_vpc.django_vpc.id

  tags = {
    Name = "DjangoIGW"
  }
}

# Create a public subnet
resource "aws_subnet" "django_public_subnet" {
  vpc_id            = aws_vpc.django_vpc.id
  cidr_block        = var.public_subnet_cidrs[0]
  availability_zone = var.availability_zones[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "DjangoPublicSubnet"
  }
}

# Create a Route Table for the public subnet
resource "aws_route_table" "django_public_rt" {
  vpc_id = aws_vpc.django_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.django_igw.id
  }

  tags = {
    Name = "DjangoPublicRT"
  }
}

# Associate the public Route Table with the public subnet
resource "aws_route_table_association" "django_a" {
  subnet_id      = aws_subnet.django_public_subnet.id
  route_table_id = aws_route_table.django_public_rt.id
}

# Define a Security Group for the EC2 instance in the VPC
resource "aws_security_group" "django_sg" {
  name        = "django_sg"
  description = "Allow web traffic to Django app"
  vpc_id      = aws_vpc.django_vpc.id

  # Allow inbound HTTP and HTTPS traffic
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Optional: Allow SSH access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidr
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "DjangoSecurityGroup"
  }
}

# RDS Subnet Group
resource "aws_db_subnet_group" "rds_subnet" {
  name       = "rds_subnet_group"
  subnet_ids = [aws_subnet.django_public_subnet.id]

  tags = {
    Name = "MyDBSubnetGroup"
  }
}

# Security Group for RDS
resource "aws_security_group" "rds_sg" {
  name        = "rds_sg"
  description = "Security group for RDS PostgreSQL"
  vpc_id      = aws_vpc.django_vpc.id

  ingress {
    from_port   = 5432  # PostgreSQL port
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # CIDR blocks that should be allowed to access the database
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds_security_group"
  }
}