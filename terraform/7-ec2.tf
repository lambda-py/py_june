data "aws_ami" "ubuntu_ami" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["*ubuntu-*-22.04-amd64-server-*"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "generated_key" {
  key_name   = "my_key_pair"
  public_key = tls_private_key.ssh_key.public_key_openssh
}

resource "aws_instance" "django_app" {
  ami                    = data.aws_ami.ubuntu_ami.id
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.generated_key.key_name
  subnet_id              = aws_subnet.django_public_subnet.id
  vpc_security_group_ids = [aws_security_group.django_sg.id]

  user_data = <<-EOF
    #!/bin/bash
    sudo apt-get update
    sudo apt-get install -y apache2
    echo 'Hello World' | sudo tee /var/www/html/index.html
    sudo systemctl start apache2
    sudo systemctl enable apache2
  EOF

  tags = {
    Name = "DjangoAppInstance"
  }
}

output "django_app_private_ip" {
  description = "The private IP of the Django application"
  value       = aws_instance.django_app.public_ip
}
