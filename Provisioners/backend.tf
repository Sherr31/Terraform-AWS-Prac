# S3 bucket was destroyed; use local state to finish cleanup.
# Re-enable after recreating the bucket if you run this lab again.
#
# terraform {
#   backend "s3" {
#     bucket       = "sherry-provisioners-tf-state"
#     key          = "provisioners/terraform.tfstate"
#     region       = "us-east-1"
#     use_lockfile = true
#   }
# }
