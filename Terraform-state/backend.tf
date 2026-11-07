terraform {
  backend "s3" {
    bucket       = "sherry-tf-state-test"
    key          = "sherrytfstate/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
  }
}
