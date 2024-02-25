resource "aws_subnet" "django_public_subnet" {
  vpc_id                  = aws_vpc.django_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "eu-west-3a"

  tags = {
    Name = "DjangoPublicSubnet"
  }
}
