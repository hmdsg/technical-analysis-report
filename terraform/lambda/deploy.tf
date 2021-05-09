resource "null_resource" "pip_install" {
    provisioner "local-exec" {
        command = "pip install requests -t TechnicalAnalysisFunction"
    }
}

data "archive_file" "TechnicalAnalysisFunction_function_zip" {
  depends_on = [null_resource.pip_install]
  type        = "zip"
  source_dir  = "TechnicalAnalysisFunction"
  output_path = "TechnicalAnalysisFunction.zip"
}


resource "aws_lambda_function" "technical-analysis-function" {
  filename         = data.archive_file.TechnicalAnalysisFunction_function_zip.output_path
  function_name    = "TechnicalAnalysisFunction"
  description      = "TechnicalAnalysisFunction"
  role             = aws_iam_role.TechnicalAnalysisFunction_iam_role.arn
  handler          = "TechnicalAnalysisFunction.lambda_handler"
  source_code_hash = data.archive_file.TechnicalAnalysisFunction_function_zip.output_base64sha256
  runtime          = "python3.8"
  timeout          = "900"
  memory_size      = "1024"
}



# Role
resource "aws_iam_role" "TechnicalAnalysisFunction_iam_role" {
  name = "TechnicalAnalysisFunction_iam_role"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
POLICY
}

# Policy
resource "aws_iam_role_policy" "TechnicalAnalysisFunction_access_policy" {
  name   = "TechnicalAnalysisFunction_lambda_access_policy"
  role   = aws_iam_role.TechnicalAnalysisFunction_iam_role.id
  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:CreateLogGroup",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
POLICY
}