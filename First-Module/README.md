<div align="center">

# Practice 01 — First Module

**EC2 · variables · outputs**

Part of [`Terraform-AWS-Prac`](../README.md)

[![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![EC2](https://img.shields.io/badge/AWS-EC2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white)](#)
[![Region](https://img.shields.io/badge/Region-us--east--1-232F3E?style=for-the-badge)](#)

</div>

---

## Purpose

First hands-on lab in this repo.

Learn the smallest useful Terraform loop:

```text
 variables  →  plan  →  apply  →  output
```

Use this folder to get comfortable before moving to remote state in [`Terraform-state/`](../Terraform-state/).

---

## Layout

```text
First-Module/
├── main.tf            provider + EC2 instance
├── vaiables.tf        input variables
├── terraform.tfvars   values for those variables
├── output.tf          public IP output
└── README.md
```

---

## Main file — `main.tf`

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "test_instance" {
  ami           = var.ami_value
  instance_type = var.instance_type_value
  tags = {
    Name = "test-instance"
  }
}
```

| Piece | What it teaches |
|-------|-----------------|
| `provider "aws"` | Where resources are created |
| `aws_instance` | Declaring compute in code |
| `var.*` | Keeping values out of hard-coded resource blocks |
| `tags` | Naming resources in the AWS console |

---

## Variables & outputs

| File | Role |
|------|------|
| `vaiables.tf` | Declares `ami_value` and `instance_type_value` |
| `terraform.tfvars` | Supplies the actual values for a local run |
| `output.tf` | Prints `aws_instance.test_instance.public_ip` |

---

## Commands

```bash
cd First-Module

terraform init
terraform plan
terraform apply

terraform output
terraform destroy   # when practice is done
```

**Do not commit** `.terraform/`, `*.tfstate`, or `*.tfstate.*`.

---

## Checklist

- [ ] `init` downloads the AWS provider
- [ ] `plan` shows one EC2 to create
- [ ] `apply` launches the instance
- [ ] `output` shows the public IP
- [ ] Instance appears in the EC2 console (`us-east-1`)
- [ ] `destroy` cleans everything up

---

## Next lab

Remote state, S3 backend, and locking → [`Terraform-state/`](../Terraform-state/)

---

<div align="center">

**First steps.** Variables in → infrastructure out.

↑ [`Back to repo`](../README.md)

</div>
