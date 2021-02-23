terraform {
  backend "s3" {
    bucket = "hamada-prd-tfstate"
    key    = "lambda/terraform.tfstate"
    region = "ap-northeast-1"
  }
}


