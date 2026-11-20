variable "ami" {
  type    = string
  default = "ami-0d97d7f07b25dd693"
}

variable "instance_type" {
  type    = map(string)
  default = {
    dev = "t3.micro"
    stage = "t3.small"
    prod = "t3.small"
  }
}