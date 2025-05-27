**If you're a candidate, you can ignore this directory.**

This is a simple Flask application that serves (hard-coded) exchange rates. It is used during our Currency Conversion interview to simulate an upstream service that we need to query.

## Building and Running the server

```bash
docker build -t currency-rates-server .
# Must be amd64 for AWS App Runner. It doesn't support ARM.
docker build --platform linux/amd64 -t currency-rates-server .
docker run -p 5555:5555 currency-rates-server
```

## Deploying the server

```bash
# Login to the braintrust interview account on the CLI using `--profile interview`
# Note: this is in us-east-2
# aws configure --profile interview sso
# aws sso login --profile interview

# Login to ECR
aws ecr get-login-password --region us-east-2 --profile interview | docker login --username AWS --password-stdin 897192298300.dkr.ecr.us-east-2.amazonaws.com
docker tag currency-rates-server:latest 897192298300.dkr.ecr.us-east-2.amazonaws.com/braintrust/currency-rates-server:latest
docker push 897192298300.dkr.ecr.us-east-2.amazonaws.com/braintrust/currency-rates-server:latest
```

A push will trigger an auto-deploy to the AWS App Runner service.
