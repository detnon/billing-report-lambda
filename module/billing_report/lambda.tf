resource "aws_lambda_function" "billing_report" {
  filename                = "./lambda.zip"
  function_name           = "${var.function_name}"
  role                    = "arn:aws:iam::1234567890:role/billing-access"
  handler                 = "lambda.lambda_handler"
  source_code_hash        = "filebase64sha256(./lambda.zip)"
  runtime                 = "python3.6"
  timeout                 = 300

}

resource "aws_cloudwatch_event_rule" "billing_report_cron_rule" {
  name                = "billing_report_cron_rule"
  description         = "Periodically gathers billing data and sends it off to splunk"
  schedule_expression = "cron(0 7 * * ? *)"
}

resource "aws_cloudwatch_event_target" "billing_report_cron_target" {
  arn       = aws_lambda_function.billing_report.arn
  target_id = aws_lambda_function.billing_report.id
  rule      = aws_cloudwatch_event_rule.billing_report_cron_rule.name
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_billing_report" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.billing_report.function_name}"

  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.billing_report_cron_rule.arn
}
