terraform {
  backend "s3" {
    bucket = "hamada-prd-tfstate"
    key    = "s3/terraform.tfstate"
    region = "ap-northeast-1"
  }
}


