resource "aws_s3_bucket" "lambda-zip-deploy" {
  bucket = "lambda-zip-deploy"
  acl    = "private"
 
  tags   = {
    Name = "lambda-zip-deploy"
  }

  versioning {
    enabled = "false"
  }
}