# Define a Security Group for the EC2 instance in the VPC
resource "aws_security_group" "django_sg" {
  name        = "django_sg"
  description = "Allow web traffic to Django app"
  vpc_id      = aws_vpc.django_vpc.id

  ingress {
    description     = "Allow http request from Load Balancer"
    protocol        = "tcp"
    from_port       = 80 # range of
    to_port         = 80 # port numbers
    security_groups = [aws_security_group.alb_sg.id]
  }

  ingress {
    description      = "Allow SSH from Bastion Host"
    protocol         = "tcp"
    from_port        = 22
    to_port          = 22
    security_groups  = [aws_security_group.bastion_sg.id]
  }

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


resource "aws_security_group" "alb_sg" {
  name        = "alb_sg"
  description = "Security group for ALB"
  vpc_id      = aws_vpc.django_vpc.id

  ingress {
    description      = "Allow http request from anywhere"
    protocol         = "tcp"
    from_port        = 80
    to_port          = 80
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    description      = "Allow https request from anywhere"
    protocol         = "tcp"
    from_port        = 443
    to_port          = 443
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ALBSecurityGroup"
  }
}