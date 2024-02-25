resource "aws_eip" "py-june_eip" {
  instance = aws_instance.django_app.id
}
