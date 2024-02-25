output "private_key_pem" {
  value     = tls_private_key.ssh_key.private_key_pem
  sensitive = true
}

output "eip_address" {
  value = aws_eip.py-june_eip.public_ip
  description = "The Elastic IP address associated with the EC2 instance"
}
