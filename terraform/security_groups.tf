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
#  ingress {
#    from_port   = 22
#    to_port     = 22
#    protocol    = "tcp"
#    cidr_blocks = var.allowed_ssh_cidr
#  }

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
