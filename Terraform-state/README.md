<div align="center">

# Practice 02 — Terraform State

**Remote state on AWS · S3 backend · locking**

Part of [`Terraform-AWS-Prac`](../README.md)

[![S3 Backend](https://img.shields.io/badge/Backend-S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)](#)
[![Lockfile](https://img.shields.io/badge/Locking-use__lockfile-232F3E?style=for-the-badge)](#)
[![Region](https://img.shields.io/badge/Region-us--east--1-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)](#)

</div>

---

## Purpose

This lab teaches **where Terraform state lives** and how teams share it safely.

You will practice:

- Creating resources that later *host* remote state
- Applying with **local** state first (bootstrap)
- Migrating state into **S3**
- Locking with **`use_lockfile`** (modern) while still creating a DynamoDB lock table for learning

> This folder is a sandbox. Experiment here, then push screenshots and notes.

---

## Layout

```text
Terraform-state/
├── mian.tf       ← main practice config (provider + resources)
├── backend.tf    ← S3 remote backend
├── pics/         ← AWS Console proof
└── README.md
```

---

## Main file — `mian.tf`

Heart of this lab. Everything Terraform creates in AWS is declared here.

### Provider

```hcl
provider "aws" {
  region = "us-east-1"
}
```

### Resources

| Block | AWS | Why it is here |
|-------|-----|----------------|
| `aws_instance.terraform_state` | **EC2** `t3.micro` | See compute appear from Terraform |
| `aws_s3_bucket.s3_bucket` | **S3** `sherry-tf-state-test` | Bucket that will store remote state |
| `aws_dynamodb_table.aws_dynamodb_table` | **DynamoDB** `terraform-state-lock` | Classic lock table (`LockID`, on-demand) |

```hcl
resource "aws_instance" "terraform_state" {
  instance_type = "t3.micro"
  ami           = "ami-0d97d7f07b25dd693"
}

resource "aws_s3_bucket" "s3_bucket" {
  bucket = "sherry-tf-state-test"
}

resource "aws_dynamodb_table" "aws_dynamodb_table" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

> **Tip:** S3 names are globally unique. On `BucketAlreadyExists`, rename or `terraform import` a bucket you already own.

---

## Backend — `backend.tf`

```hcl
terraform {
  backend "s3" {
    bucket       = "sherry-tf-state-test"
    key          = "sherrytfstate/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
  }
}
```

| Setting | Meaning |
|---------|---------|
| `bucket` | S3 bucket holding state |
| `key` | Object path for `terraform.tfstate` |
| `region` | Bucket region |
| `use_lockfile` | S3-native lock (preferred over deprecated `dynamodb_table`) |

---

## Bootstrap flow

```text
 ┌──────────────────┐
 │ Comment backend  │  apply with LOCAL state
 └────────┬─────────┘
          ▼
 ┌──────────────────┐
 │ Create S3 (+ DDB)│  resources exist in AWS
 └────────┬─────────┘
          ▼
 ┌──────────────────┐
 │ Enable backend   │  terraform init -migrate-state
 └────────┬─────────┘
          ▼
 ┌──────────────────┐
 │ State in S3      │  lockfile protects concurrent applies
 └──────────────────┘
```

---

## Commands

```bash
cd Terraform-state

terraform init
terraform plan
terraform apply

# after enabling backend.tf
terraform init -migrate-state

terraform state list
terraform destroy    # clean up when practice is done
```

**Do not commit** `terraform.tfstate`, `*.tfstate.*`, or `.terraform/`.

---

## Console proof

<table>
  <tr>
    <td align="center" width="50%">
      <img src="pics/s3-2.png" alt="S3 buckets" />
      <br /><sub><b>S3</b> — buckets</sub>
    </td>
    <td align="center" width="50%">
      <img src="pics/s3-1.png" alt="State file in S3" />
      <br /><sub><b>S3</b> — <code>terraform.tfstate</code> object</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <img src="pics/Dynomodb.png" alt="DynamoDB table" />
      <br /><sub><b>DynamoDB</b> — <code>terraform-state-lock</code></sub>
    </td>
    <td align="center" width="50%">
      <img src="pics/ec2.png" alt="EC2 instance" />
      <br /><sub><b>EC2</b> — running instance</sub>
    </td>
  </tr>
</table>

---

## Checklist

- [ ] `apply` creates EC2, S3, and DynamoDB from `mian.tf`
- [ ] Understand why laptop-only state is risky
- [ ] Migrate local → S3 with `-migrate-state`
- [ ] See state object in the S3 console
- [ ] Know `use_lockfile` vs DynamoDB locking
- [ ] `destroy` so practice does not keep costing money

---

<div align="center">

**State sandbox.** Edit → apply → observe → push.

↑ [`Back to repo`](../README.md)

</div>
