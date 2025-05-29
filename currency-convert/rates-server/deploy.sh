#!/bin/bash

# Variables
PROFILE="interview"
REGION="us-east-2"
ACCOUNT_ID="897192298300"
SERVICE_ARN="arn:aws:apprunner:$REGION:$ACCOUNT_ID:service/currency-rates-server/0b28096acd824b75b00ea532835eee84"
ECR_REPO="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/braintrust/currency-rates-server:latest"
LOCAL_IMAGE="currency-rates-server:latest"

# Function to check and report App Runner status
check_status() {
  echo "Checking App Runner deployment status..."
  MAX_WAIT=30
  INTERVAL=5
  ELAPSED=0

  while [ $ELAPSED -lt $MAX_WAIT ]; do
    STATUS=$(aws --profile $PROFILE apprunner describe-service --service-arn $SERVICE_ARN --query 'Service.Status' --output text)
    echo "Status: $STATUS (Elapsed: ${ELAPSED}s)"

    if [ "$STATUS" != "OPERATION_IN_PROGRESS" ]; then
      echo "Deployment finished with status: $STATUS"
      exit 0
    fi

    sleep $INTERVAL
    ELAPSED=$((ELAPSED + INTERVAL))
  done

  echo "Deployment still in progress after ${MAX_WAIT}s."
}

# Handle --status flag
if [ "$1" == "--status" ]; then
  check_status
  exit 0
fi

# 1. Authenticate Docker to ECR
aws ecr get-login-password --region $REGION --profile $PROFILE | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# 2. Tag and push Docker image
docker tag $LOCAL_IMAGE $ECR_REPO
docker push $ECR_REPO

# 3. Poll App Runner deployment status for up to 30s
check_status
