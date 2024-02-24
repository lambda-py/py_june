resource "aws_internet_gateway" "django_igw" {
  vpc_id = aws_vpc.django_vpc.id
  tags   = {
    Name = "DjangoIGW"
  }
}

# Public Route Table
resource "aws_route_table" "django_public_rt" {
  vpc_id = aws_vpc.django_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.django_igw.id
  }

  tags = {
    Name = "DjangoPublicRT"
  }
}

# Associate Public Subnet with Public Route Table
resource "aws_route_table_association" "django_public_rta" {
  subnet_id      = aws_subnet.alb_public_subnet2.id
  route_table_id = aws_route_table.django_public_rt.id
}
