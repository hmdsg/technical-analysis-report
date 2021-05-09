terraform {
  backend "s3" {
    bucket = "tar-sys-terraform"
    key    = "lambda/terraform.tfstate"
    region = "ap-northeast-1"
  }
}


