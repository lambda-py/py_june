resource "aws_s3_bucket" "bucket" {
  bucket     = "s3-logs"
  bucket_acl = "private"

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}