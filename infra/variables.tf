variable "aws_region" {
  description = "AWS region to deploy into."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name prefix for all resources."
  type        = string
  default     = "idea-evaluator"
}

variable "anthropic_api_key" {
  description = "Anthropic API key passed to the Lambda as an environment variable."
  type        = string
  sensitive   = true
}

variable "lambda_memory_mb" {
  description = "Memory (MB) for the evaluator Lambda."
  type        = number
  default     = 512
}

variable "lambda_timeout_s" {
  description = "Timeout (seconds) for the evaluator Lambda. Must exceed a Claude call (~27s)."
  type        = number
  default     = 60
}
