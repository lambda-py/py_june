resource "aws_instance" "django_app" {
  ami           = var.ubuntu_yammy_ami
  instance_type = var.instance_type

  # Associate the instance with a security group
  vpc_security_group_ids = [aws_security_group.django_sg.id]

  # Specify the subnet ID to launch the instance in a specific subnet within your VPC
  subnet_id = aws_subnet.django_public_subnet.id

  # Block device mappings - optional, customize if you need additional storage
  block_device_mappings {
    device_name = "/dev/sda1"
    ebs {
      volume_size = 20  # Volume size in GB
      volume_type = "gp2"  # General Purpose SSD
      delete_on_termination = true
    }
  }

  # User data script to install and configure necessary software upon instance initialization
  user_data = file("${path.module}/setup.sh")

  # Tags for resource identification and management
  tags = {
    Name = "DjangoAppInstance"
  }
}
