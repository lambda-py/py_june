resource "aws_route53_zone" "main" {
  name = "py-june.dev"
}

resource "aws_route53_record" "a_record" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "py-june.dev"
  type    = "A"
  ttl     = "300"
  records = [aws_eip.py-june_eip.public_ip]
}

resource "aws_route53_record" "www_cname" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.py-june.dev"
  type    = "CNAME"
  ttl     = "300"
  records = ["py-june.dev"]
}
