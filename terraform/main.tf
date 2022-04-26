terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-west-2"
}

resource "aws_s3_bucket" "b" {
  bucket = "labor-stats"
}

resource "aws_s3_bucket_acl" "example" {
  bucket = aws_s3_bucket.b.id
  acl    = "private"
}

resource "aws_db_instance" "default" {
  allocated_storage    = 10
  engine               = "postgres"
  engine_version       = "11.5"
  instance_class       = "db.t3.micro"
  identifier           = "labor-stats2"
  name                 = var.dbname
  username             = var.dbusername
  password             = var.dbpw
  publicly_accessible  = true
}