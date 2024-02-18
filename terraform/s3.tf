resource "aws_s3_bucket" "bucket" {
  bucket     = "s3-logs-bucket-12345"

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_public_access_block" "access_block" {
  bucket = aws_s3_bucket.bucket.id

  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls  = true
  restrict_public_buckets = true
}

data "aws_elb_service_account" "main" {}

resource "aws_s3_bucket_policy" "bucket_policy" {
  bucket = aws_s3_bucket.bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "ELBAccessLogsWrite"
        Effect    = "Allow"
        Principal = {
          AWS = data.aws_elb_service_account.main.arn
        }
        Action   = "s3:PutObject"
        Resource = "${aws_s3_bucket.bucket.arn}/*"
      },
      {
        Sid       = "ELBAccessLogsRead"
        Effect    = "Allow"
        Principal = {
          AWS = data.aws_elb_service_account.main.arn
        }
        Action   = ["s3:GetBucketAcl", "s3:GetBucketPolicy"]
        Resource = aws_s3_bucket.bucket.arn
      }
    ]
  })
}
