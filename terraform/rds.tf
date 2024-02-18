resource "aws_db_instance" "django_db" {
  allocated_storage    = 20  # The size of the database (in gigabytes)
  storage_type         = "gp2"
  engine               = "postgres"  # Specify the database engine
  engine_version       = "15.5"  # Use the appropriate version for your needs
  instance_class       = "db.t3.micro"  # Choose the instance class
  db_name              = var.db_name
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.postgres15"

  # Network & Security
  vpc_security_group_ids = [aws_security_group.rds_sg.id]  # Security group for RDS
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name  # DB subnet group

  # Backup
  backup_retention_period = 7  # Number of days to retain backups
  backup_window           = "03:00-06:00"

  # Maintenance
  maintenance_window         = "Sun:07:00-Sun:10:00"
  auto_minor_version_upgrade = true

  # Deletion protection and multi-AZ
  deletion_protection = false
  multi_az            = false

  # Tags
  tags = {
    Name = "DjangoRDS"
  }
}