provider "aws" {
  region = "us-east-1"
}

module "ec2" {
  source = "./Modules/ec2"
  ami           = var.ami
  instance_type = lookup(var.instance_type, terraform.workspace, "t3.small")
  # ami           = var.ami
  # instance_type = var.instance_type
}
