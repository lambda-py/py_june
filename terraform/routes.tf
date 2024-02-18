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
  subnet_id      = aws_subnet.django_public_subnet.id
  route_table_id = aws_route_table.django_public_rt.id
}

# EIP for NAT Gateway
resource "aws_eip" "nat_eip" {
  depends_on = [aws_internet_gateway.django_igw]
  domain     = "vpc"

  tags = {
    Name = "DjangoNATGatewayEIP"
  }
}

# A NAT Gateway: This allows instances in your private subnet to access
# the internet for updates and patches, while still keeping them private.
# (for the private subnet to access internet - eg. ec2 instances downloading softwares from internet)
resource "aws_nat_gateway" "django_nat_gw" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.django_public_subnet.id

  tags = {
    Name = "DjangoNATGateway"
  }

  depends_on = [aws_internet_gateway.django_igw]
}

# Private Route Table
resource "aws_route_table" "django_private_rt" {
  vpc_id = aws_vpc.django_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.django_nat_gw.id
  }

  tags = {
    Name = "DjangoPrivateRT"
  }
}

# Associate Private Subnet with Private Route Table
resource "aws_route_table_association" "django_private_rta" {
  subnet_id      = aws_subnet.django_private_subnet.id
  route_table_id = aws_route_table.django_private_rt.id
}
