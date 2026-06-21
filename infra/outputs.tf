output "cloudfront_url" {
  description = "Public URL for the deployed app."
  value       = "https://${aws_cloudfront_distribution.cdn.domain_name}"
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID (for cache invalidation)."
  value       = aws_cloudfront_distribution.cdn.id
}

output "frontend_bucket" {
  description = "S3 bucket holding the frontend build."
  value       = aws_s3_bucket.frontend.bucket
}

output "api_function_url" {
  description = "Direct Lambda Function URL (CloudFront proxies /api/* here)."
  value       = aws_lambda_function_url.api.function_url
}
