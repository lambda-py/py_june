# Create a Route Table for the public subnet
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

# Associate the public Route Table with the public subnet
resource "aws_route_table_association" "django_a" {
  subnet_id      = aws_subnet.django_public_subnet.id
  route_table_id = aws_route_table.django_public_rt.id
}
