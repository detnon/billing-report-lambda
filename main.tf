terraform {
  backend "s3" {
    bucket  = ""
    key     = ""
    region  = "eu-west-2"
    encrypt = true
  }
}

module "active_accounts_checker" {
  function_name        = "billing_report"
  source               = "./module/billing_report"
}
