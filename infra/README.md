# Deployment (AWS, Terraform)

Deploys the Idea Evaluator to AWS account `237414921190` in `us-east-1`.

## Architecture

```
Browser ──HTTPS──► CloudFront ──┬── default behavior ──► S3 (private, OAC)        [static frontend]
                                └── /api/* behavior ───► Lambda Function URL (OAC) [FastAPI via Mangum]
                                                              └──► Claude (claude-sonnet-4-6)
```

- **Backend**: FastAPI (`backend/main.py`) wrapped with Mangum, on Lambda (Python 3.13).
  Fronted by a **Lambda Function URL**, not API Gateway, because API Gateway HTTP
  APIs cap integration time at 30s and a Claude evaluation takes ~27s.
- **Frontend**: Vite/React build in a private S3 bucket, served via CloudFront.
- **Auth**: The Function URL uses `AWS_IAM`; CloudFront signs origin requests with
  **Origin Access Control (OAC)**. The URL is not publicly reachable.

## Deploy

```bash
# 1. Build the Lambda package (Docker; produces Linux x86_64 wheels)
./build_lambda.sh

# 2. Provision / update infrastructure
export TF_VAR_anthropic_api_key="$(grep -E '^ANTHROPIC_API_KEY=' ../backend/.env | cut -d= -f2-)"
terraform init      # first time only
terraform apply

# 3. Build + publish the frontend, then invalidate the CDN
./deploy_frontend.sh
```

`terraform output cloudfront_url` prints the public app URL.

## Gotchas (OAC → Lambda function URL)

These took real debugging; do not "simplify" them away:

1. **Client must send `x-amz-content-sha256`** = hex SHA-256 of the exact request
   body. CloudFront OAC does *not* hash bodies itself and Lambda rejects unsigned
   payloads, so without this header every POST fails with *"signature does not
   match"*. The frontend computes it in `App.jsx`. You cannot add this header to a
   CloudFront origin request policy (CloudFront rejects it) — it is handled
   automatically when the client sends it.
2. **Two Lambda permissions** are required for the CloudFront service principal:
   `lambda:InvokeFunctionUrl` *and* `lambda:InvokeFunction`. With only the first,
   a correctly-signed request still returns *"Forbidden"*.
3. **Public function URLs (`AuthType=NONE`) are blocked** in this account, which is
   why OAC + `AWS_IAM` is used instead.
4. Lambda timeout (60s) and CloudFront `origin_read_timeout` (60s) must both exceed
   the ~27s Claude call.
