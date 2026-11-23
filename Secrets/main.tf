provider "aws" {
  region = "us-east-1"
}

provider "vault" {
  address = "http://174.129.90.245:8200"
  skip_child_token = true

  auth_login {
    path = "auth/approle/login"

    parameters = {
      role_id = "88b4e611-c161-024f-7605-ddf7d60bb95e"
      secret_id = "33122790-8b17-fbc8-1481-119ceca6bdad"
    }
  }
}

data "vault_kv_secret_v2" "example" {
  mount = "test-secret" // change it according to your mount
  name  = "test-secret" // change it according to your secret
}

resource "aws_instance" "my_instance" {
  ami           = "ami-053b0d53c279acc90"
  instance_type = "t3.micro"

  tags = {
    Name = "test"
    Secret = data.vault_kv_secret_v2.example.data["secrets"]
  }
}