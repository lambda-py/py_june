resource "aws_instance" "django_app" {
  ami           = var.ubuntu_focal_ami
  instance_type = var.instance_type

  # Associate the instance with a security group
  vpc_security_group_ids = [aws_security_group.django_sg.id]

  # Specify the subnet ID to launch the instance in a specific subnet within your VPC
  subnet_id = aws_subnet.django_public_subnet.id

  # ebs block - optional, customize if you need additional storage
  ebs_block_device {
    device_name = "/dev/sdm"
    volume_size = 20
    volume_type = "gp2"
    delete_on_termination = true
  }

  # User data script to install and configure necessary software upon instance initialization
  user_data = file("${path.module}/setup.sh")

  # Tags for resource identification and management
  tags = {
    Name = "DjangoAppInstance"
  }
}
