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

provider "vault" {
  address = "<>:8200"
  skip_child_token = true

  auth_login {
    path = "auth/approle/login"

    parameters = {
      role_id = "343c0b71-a5a9-2226-0a8c-a24b06345435"
      secret_id = "76775f79-8515-ca3a-d91e-036f9cdf6c4f"
    }
  }
}

data "vault_kv_secret_v2" "example" {
  mount = "343c0b71-a5a9-2226-0a8c-a24b06345435" // change it according to your mount
  name  = "test-secret" // change it according to your secret
}

resource "aws_instance" "my_instance" {
  ami           = "ami-053b0d53c279acc90"
  instance_type = "t3.micro"

  tags = {
    Name = "test"
    Secret = data.vault_kv_secret_v2.example.data["foo"]
  }
}