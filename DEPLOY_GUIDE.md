# Deployment to Cloud Guide

## Overview
This guide provides step‑by‑step instructions for deploying the Deep Learning application to a cloud environment (AWS, Azure, or GCP). It covers prerequisites, Docker image creation, infrastructure provisioning, CI/CD integration, verification, and cleanup.

## Prerequisites
- Cloud account with appropriate permissions (AWS IAM, Azure Service Principal, or GCP Service Account).
- Docker installed locally.
- Terraform or CloudFormation installed for infrastructure as code.
- Access to the GitHub repository `deep_learning`.
- Environment variables for cloud credentials set in your CI/CD system.

## 1. Docker Image Build & Push
```bash
# Build Docker image
docker build -t your-registry/your-image:latest .

# Login to container registry (example for AWS ECR)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag your-image:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/your-image:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/your-image:latest
```

## 2. Infrastructure Provisioning
Choose your IaC tool:
- **Terraform** (cloud‑agnostic)
- **AWS CloudFormation**
- **Azure Resource Manager (ARM) templates)**
- **Google Deployment Manager**

Example Terraform snippet for an AWS ECS service:
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_ecs_cluster" "cluster" {
  name = "deep-learning-cluster"
}

resource "aws_ecs_task_definition" "task" {
  family                   = "deep-learning-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  container_definitions = jsonencode([
    {
      name  = "app"
      image = "<account-id>.dkr.ecr.us-east-1.amazonaws.com/your-image:latest"
      essential = true
      portMappings = [{ containerPort = 80 }]
    }
  ])
}
```
Apply with:
```bash
terraform init
terraform apply
```

## 3. CI/CD Pipeline Integration
Add the following steps to your CI workflow (GitHub Actions example):
```yaml
name: CI/CD
on:
  push:
    branches: [ main ]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      - name: Log in to Amazon ECR
        uses: aws-actions/amazon-ecr-login@v1
      - name: Build and push Docker image
        run: |
          docker build -t ${{ env.ECR_REGISTRY }}/your-image:latest .
          docker push ${{ env.ECR_REGISTRY }}/your-image:latest
      - name: Deploy with Terraform
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          terraform init
          terraform apply -auto-approve
```

## 4. Verification & Monitoring
- Verify the service is running via the cloud console or CLI.
- Use CloudWatch (AWS), Azure Monitor, or Stackdriver (GCP) for logs and metrics.
- Perform a health‑check request:
```bash
curl https://<your-service-endpoint>/health
```

## 5. Cleanup
When the deployment is no longer needed, destroy resources:
```bash
terraform destroy -auto-approve
```
Or delete the service via the cloud console.

---
*This document is version‑controlled. Update as needed for specific cloud provider nuances.*