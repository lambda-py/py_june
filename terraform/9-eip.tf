resource "aws_eip" "my_eip" {
  instance = aws_instance.django_app.id
}
