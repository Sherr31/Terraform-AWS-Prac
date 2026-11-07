
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "test_instance" {
  ami           = var.ami_value  # Ubuntu 20.04 LTS
  instance_type = var.instance_type_value
  tags = {
    Name = "test-instance"
  }
}