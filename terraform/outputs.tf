output "django_app_private_ip" {
  description = "The private IP of the Django application"
  value       = aws_instance.django_app.private_ip
}

# Output for RDS Instance Endpoint
output "rds_instance_endpoint" {
  description = "The connection endpoint for the RDS database instance."
  value       = aws_db_instance.django_db.endpoint
}

# Optional: Output for RDS Instance Name
output "rds_instance_name" {
  description = "The name of the RDS database instance."
  value       = aws_db_instance.django_db.db_name
}

# Optional: Output for Security Group ID used by EC2 Instance
output "ec2_security_group_id" {
  description = "The ID of the security group attached to the EC2 instance."
  value       = aws_security_group.django_sg.id
}

# Optional: Output for VPC ID
output "vpc_id" {
  description = "The ID of the VPC where resources are deployed."
  value       = aws_vpc.django_vpc.id
}

output "alb_dns_name" {
  description = "The DNS name of the Application Load Balancer."
  value       = aws_lb.django_alb.dns_name
}

output "private_key" {
  description = "The private key for SSH access"
  value       = tls_private_key.ssh_key.private_key_pem
  sensitive   = true
}

output "bastion_host_public_ip" {
  description = "The public IP of the bastion host"
  value       = aws_instance.bastion_host.public_ip
}
