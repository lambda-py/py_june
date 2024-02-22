resource "aws_lb" "django_alb" {
  name               = "django-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [aws_subnet.django_public_subnet.id]
  depends_on         = [aws_internet_gateway.django_igw]

  #  access_logs {
  #    bucket  = aws_s3_bucket.bucket.bucket
  #    prefix  = "alb-logs"
  #    enabled = true
  #  }

  tags = {
    Name = "django-alb"
  }
}

resource "aws_lb_target_group" "django_alb_tg" {
  name     = "django-alb-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.django_vpc.id
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

resource "aws_lb_target_group_attachment" "django_alb_tg_attachment" {
  target_group_arn = aws_lb_target_group.django_alb_tg.arn
  target_id        = aws_instance.django_app.id
  port             = 80
}
