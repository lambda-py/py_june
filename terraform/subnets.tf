# Create a public subnet
resource "aws_subnet" "django_public_subnet" {
  vpc_id            = aws_vpc.django_vpc.id
  cidr_block        = var.public_subnet_cidrs[0]
  availability_zone = var.availability_zones[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "PublicSubnet"
  }
}

resource "aws_subnet" "django_public_subnet2" {
  vpc_id            = aws_vpc.django_vpc.id
  cidr_block        = var.public_subnet_cidrs[1]
  availability_zone = var.availability_zones[1]
  map_public_ip_on_launch = true

  tags = {
    Name = "PublicSubnet2"
  }
}

resource "aws_subnet" "django_private_subnet" {
  vpc_id            = aws_vpc.django_vpc.id
  cidr_block        = var.private_subnet_cidrs[0]
  availability_zone = var.availability_zones[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "DjangoPrivateSubnet"
  }
}

resource "aws_subnet" "rds_private_subnet" {
  vpc_id            = aws_vpc.django_vpc.id
  cidr_block        = var.private_subnet_cidrs[1]
  availability_zone = var.availability_zones[1]

  tags = {
    Name = "RDSPrivateSubnet"
  }
}


# RDS Subnet Group
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "rds_subnet_group"
  subnet_ids = [aws_subnet.django_private_subnet.id, aws_subnet.rds_private_subnet.id]

  tags = {
    Name = "RDSSubnetGroup"
  }
}
