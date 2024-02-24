resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "generated_key" {
  key_name   = "my_key_pair"
  public_key = tls_private_key.ssh_key.public_key_openssh
}

resource "aws_instance" "django_app" {
  ami           = data.aws_ami.ubuntu_ami.id
  instance_type = var.instance_type
  key_name      = aws_key_pair.generated_key.key_name

  # Associate the instance with a security group
  vpc_security_group_ids = [aws_security_group.django_sg.id]

  # Specify the subnet ID to launch the instance in a specific subnet within your VPC
  subnet_id = aws_subnet.django_private_subnet.id

  # User data script to install and configure necessary software upon instance initialization
  #  user_data = file("${path.module}/setup.sh")
  user_data = <<-EOF
     #!/bin/bash
     sudo su
     apt-get update -y
     apt-get install apache2 -y
     systemctl start apache2
     systemctl enable apache2
     echo "<h1>loading from $(hostname -f)..</h1>" > /var/www/html/index.html
  EOF
  # Tags for resource identification and management
  tags      = {
    Name = "DjangoAppInstance"
  }
}

resource "aws_security_group" "bastion_sg" {
  name        = "bastion_sg"
  description = "Security group for Bastion Host"
  vpc_id      = aws_vpc.django_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["95.214.217.183/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "BastionHostSecurityGroup"
  }
}

resource "aws_instance" "bastion_host" {
  ami           = data.aws_ami.ubuntu_ami.id
  instance_type = "t2.micro"
  key_name      = aws_key_pair.generated_key.key_name

  vpc_security_group_ids = [aws_security_group.bastion_sg.id]
  subnet_id              = aws_subnet.django_public_subnet.id

  tags = {
    Name = "BastionHost"
  }
}

resource "aws_security_group_rule" "allow_ssh_from_bastion_to_app" {
  type                     = "ingress"
  from_port                = 22
  to_port                  = 22
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.bastion_sg.id
  security_group_id        = aws_security_group.django_sg.id
}