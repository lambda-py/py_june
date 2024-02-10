# Create a public subnet
resource "aws_subnet" "django_public_subnet" {
  vpc_id            = aws_vpc.django_vpc.id
  cidr_block        = var.public_subnet_cidrs[0]
  availability_zone = var.availability_zones[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "DjangoPublicSubnet"
  }
}

# RDS Subnet Group
resource "aws_db_subnet_group" "rds_subnet" {
  name       = "rds_subnet_group"
  subnet_ids = [aws_subnet.django_public_subnet.id]

  tags = {
    Name = "MyDBSubnetGroup"
  }
}
