#!/usr/bin/env bash
# Builds the React frontend and publishes it to the S3 bucket created by
# Terraform, then invalidates the CloudFront cache. Run AFTER `terraform apply`.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
FRONTEND_DIR="$PROJECT_DIR/frontend"

BUCKET="$(terraform -chdir="$SCRIPT_DIR" output -raw frontend_bucket)"
DIST_ID="$(terraform -chdir="$SCRIPT_DIR" output -raw cloudfront_distribution_id)"

echo ">> Building frontend"
(cd "$FRONTEND_DIR" && npm install && npm run build)

echo ">> Syncing dist/ to s3://$BUCKET"
aws s3 sync "$FRONTEND_DIR/dist" "s3://$BUCKET" --delete

echo ">> Invalidating CloudFront cache ($DIST_ID)"
aws cloudfront create-invalidation --distribution-id "$DIST_ID" --paths "/*" >/dev/null

echo ">> Frontend deployed. App URL:"
terraform -chdir="$SCRIPT_DIR" output -raw cloudfront_url
echo
