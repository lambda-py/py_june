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
  domain = "vpc"
}

resource "aws_lb" "django_alb" {
  name               = "django-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.django_sg.id]
  subnets            = [aws_subnet.django_public_subnet.id, aws_subnet.django_public_subnet2.id]

  enable_deletion_protection = true

  access_logs {
    bucket  = "s3-logs"
    prefix  = "alb-logs"
    enabled = true
  }

  tags = {
    Name = "django-alb"
  }
}

resource "aws_lb_listener" "django_alb_listener" {
  load_balancer_arn = aws_lb.django_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.django_alb_tg.arn
  }
}

resource "aws_lb_target_group" "django_alb_tg" {
  name     = "django-alb-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.django_vpc.id

  health_check {
    enabled             = true
    interval            = 30
    path                = "/"
    timeout             = 3
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }
}

resource "aws_lb_target_group_attachment" "django_alb_tg_attachment" {
  target_group_arn = aws_lb_target_group.django_alb_tg.arn
  target_id        = aws_instance.django_app.id
  port             = 80
}
