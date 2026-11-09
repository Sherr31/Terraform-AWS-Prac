# Keep this commented until the S3 bucket exists, then uncomment and run:
#   terraform init -migrate-state

terraform {
  backend "s3" {
    bucket       = "sherry-provisioners-tf-state"
    key          = "provisioners/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
  }
}
