resource "aws_internet_gateway" "django_igw" {
  vpc_id = aws_vpc.django_vpc.id

  tags = {
    Name = "DjangoIGW"
  }
}
