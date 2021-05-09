# DynamoDB Tables
resource "aws_dynamodb_table" "premarket-price-table" {
  name           = "premarket-price"
  read_capacity  = "1"
  write_capacity = "1"

  attribute {  
    name = "timestamp"
    type = "N"
  }

  attribute {
    name = "ticker"
    type = "S"
  }

  attribute {
    name = "price"
    type = "N"
  }


}