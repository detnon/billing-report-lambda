//data "aws_iam_policy_document" "billing_report_role" {
//  statement {
//    effect  = "Allow"
//    actions = ["sts:AssumeRole"]
//
//    principals {
//      type        = "Service"
//      identifiers = ["lambda.amazonaws.com"]
//    }
//  }
//}
//
//resource "aws_iam_role" "billing_report_execution_role" {
//  name               = "billing_report_execution_role"
//  assume_role_policy = data.aws_iam_policy_document.billing_report_role.json
//}
