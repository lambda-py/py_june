# A NAT Gateway: This allows instances in your private subnet to access
# the internet for updates and patches, while still keeping them private.
resource "aws_nat_gateway" "django_nat_gw" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.django_public_subnet.id

  tags = {
    Name = "DjangoNATGateway"
  }
}

# EIP for NAT Gateway
resource "aws_eip" "nat_eip" {
  vpc = true
}

# Elastic Load Balancer
resource "aws_elb" "django_elb" {
  name               = "django-elb"
  subnets            = [aws_subnet.django_public_subnet.id]

  listener {
    instance_port     = 80
    instance_protocol = "http"
    lb_port           = 80
    lb_protocol       = "http"
  }

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    target              = "HTTP:80/"
    interval            = 30
  }

  instances                   = [aws_instance.django_app.id]
  cross_zone_load_balancing   = true
  idle_timeout                = 400
  connection_draining         = true
  connection_draining_timeout = 400

  tags = {
    Name = "DjangoELB"
  }
}