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
  key_name      = "existing_key_pair_name"

  # Associate the instance with a security group
  vpc_security_group_ids = [aws_security_group.django_sg.id]

  # Specify the subnet ID to launch the instance in a specific subnet within your VPC
  subnet_id = aws_subnet.django_public_subnet.id

  # User data script to install and configure necessary software upon instance initialization
  #  user_data = file("${path.module}/setup.sh")
  user_data = <<-EOF
     #!/bin/bash
     sudo su
     yum update -y
     yum install httpd -y
     systemctl start httpd
     systemctl enable httpd
     echo "<h1>loading from $(hostname -f)..</h1>" > /var/www/html/index.html
  EOF
  # Tags for resource identification and management
  tags      = {
    Name = "DjangoAppInstance"
  }
}
