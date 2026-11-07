provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "terraform_state" {
  instance_type = "t3.micro"
  ami = "ami-0d97d7f07b25dd693"
}

resource "aws_s3_bucket" "s3_bucket" {
  bucket = "sherry-tf-state-test"
}

resource "aws_dynamodb_table" "aws_dynamodb_table" {
name = "terraform-state-lock"
billing_mode = "PAY_PER_REQUEST"
hash_key = "LockID"

attribute {
  name = "LockID"
  type = "S"
}
}