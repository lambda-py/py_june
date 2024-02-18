resource "aws_route53_zone" "primary" {
  name = "py-june.dev"
}

resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.primary.zone_id
  name    = "www.py-june.dev"
  type    = "A"
  alias {
    name                   = aws_elb.django_elb.dns_name
    zone_id                = aws_elb.django_elb.zone_id
    evaluate_target_health = true
  }
}