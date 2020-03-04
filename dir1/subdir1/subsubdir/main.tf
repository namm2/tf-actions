resource "google_service_account" "default" {
  account_id         = "default"
  display_name   = "default"
  project      = var.project
}
