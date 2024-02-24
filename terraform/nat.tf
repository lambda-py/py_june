resource "aws_eip" "nat" {
  domain = "vpc"
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.alb_public_subnet.id
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.django_private_subnet.id
  route_table_id = aws_vpc.django_vpc.main_route_table_id
}

resource "aws_route" "private_nat_gateway" {
  route_table_id         = aws_vpc.django_vpc.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat.id
}
