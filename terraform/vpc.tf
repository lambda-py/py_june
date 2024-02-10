resource "aws_vpc" "django_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "DjangoVPC"
  }
}

resource "aws_internet_gateway" "django_igw" {
  vpc_id = aws_vpc.django_vpc.id
  tags = {
    Name = "DjangoIGW"
  }
}
