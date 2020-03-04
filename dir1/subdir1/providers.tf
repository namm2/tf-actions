provider "google" {
  version = "~> 2.20"
  project         = var.gce_project
  region      = var.gce_region
}

provider "aws" {}
