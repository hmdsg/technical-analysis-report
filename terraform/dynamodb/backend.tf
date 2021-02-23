terraform {
  backend "s3" {
    bucket = "hamada-prd-tfstate"
    key    = "dynamodb/terraform.tfstate"
    region = "ap-northeast-1"
  }
}


