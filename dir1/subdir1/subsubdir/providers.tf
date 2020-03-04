provider "google" {
  version = "~> 2.20"
  project = var.project
  region  = var.region
}

provider "aws" {}
