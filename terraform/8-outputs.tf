output "django_app_public_ip" {
  description = "The private IP of the Django application"
  value       = aws_instance.django_app.public_ip
}

output "private_key_pem" {
  value     = tls_private_key.ssh_key.private_key_pem
  sensitive = true
}
