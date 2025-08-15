[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-ready-blue.svg)](https://kubernetes.io/)


# 🚀 Docker S3 FastAPI – Data API

A simple Python (FastAPI) application that retrieves a `data.json` file from AWS S3 and serves it via an HTTP endpoint.


## ✨ Features
- **REST API with FastAPI** – lightweight, high-performance Python web framework
- **AWS S3 integration** – secure access to bucket data
- **Dockerized** – portable, reproducible environments
- **AWS ECR deployment** – store and run Docker images in the cloud
- **Unit tested** – verified functionality before deployment
- **Environment variable configuration** – flexible and cloud-friendly
- **Kubernetes/Helm ready** – project can be deployed to K8s cluster with Helm chart (example provided)

⚠️ This project is for educational and portfolio purposes only.

---

## 💼 Business Context

This project demonstrates serving analytics-ready data from S3 to internal teams via a REST API.
It simulates a real-world workflow of a Data Engineer + DevOps collaboration:
- Preparing data in S3
- Exposing it via a secure REST API
- Containerizing and deploying to cloud infrastructure
- Automating deployment with ECR/Kubernetes

---

## 📦 Project Structure
```
.
├── app
│   └── main.py           # Main FastAPI application
├── tests
│   └── test_app.py       # Unit tests
├── helm                  # Helm Chart for K8s deployment
│   └── docker-s3-fastapi
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates
│           ├── deployment.yaml
│           └── service.yaml
├── Dockerfile            # Docker build instructions
├── README.md
├── requirements.txt      # Python dependencies
```

---

## 🧪 Local Test – Python venv

### Login with AWS profile:
```bash
aws sso login --profile <profile>
```

### Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
### Install dependencies
```bash
pip install -r requirements.txt
```
### Environment variables
Ensure .env is created (not included in Git Repo):
```bash
S3_BUCKET=<s3_bucket>
AWS_REGION=<aws_region>
AWS_PROFILE=<profile>
```

### Run the application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```
### Test in web browser:
```bash
http://localhost:8080/ → "Data API is running!"
http://localhost:8080/data → attempts to download data.json from S3
```

## 🐳 Local Test – Docker
> ⚠️ Note: Make sure Docker Desktop is running.

Build Docker image:
```bash
docker build -t docker-s3-fastapi .
```
Run Docker container using created image:
```bash
docker run --env-file .env -p 8080:8080 \
  -v ~/.aws:/root/.aws:ro \
  -e AWS_PROFILE=<profile> \
  -e S3_BUCKET=<s3_bucket> \
  -e AWS_REGION=<aws_region> \
  docker-s3-fastapi
```
### Test in web browser:

```
http://localhost:8080/data
```

## 🧪 Unit Tests:

Run in terminal:
```bash
pytest tests/test_app.py  
```

## 📤 Deploying to AWS ECR
### Create ECR repository:
```bash
aws ecr create-repository \
    --repository-name docker-s3-fastapi \
    --region <aws_region> \
    --profile <profile>
```

### Authenticate Docker to ECR
```bash
aws ecr get-login-password \
    --region <aws_region> \
    --profile <profile> \
  | docker login \
    --username AWS \
    --password-stdin <account_id>.dkr.ecr.<aws_region>.amazonaws.com
```

### Build and tag the image
```bash
docker build -t docker-s3-fastapi .
docker tag docker-s3-fastapi:latest <account_id>.dkr.ecr.<aws_region>.amazonaws.com/docker-s3-fastapi:latest
```

### Push the image to ECR
```bash
docker push <account_id>.dkr.ecr.<aws_region>.amazonaws.com/docker-s3-fastapi:latest
```

### Run the image from ECR
```bash
docker run -p 8080:8080 \
  -v ~/.aws:/root/.aws:ro \
  -e AWS_PROFILE=<profile> \
  -e S3_BUCKET=<s3_bucket> \
  -e AWS_REGION=<aws_region> \
  <account_id>.dkr.ecr.<aws_region>.amazonaws.com/docker-s3-fastapi:latest
```
### Test in web browser:

```
http://localhost:8080/data
```

## 🛠 Helm Chart – Local Test with Kind

### Create a Local Kubernetes Cluster (assuming Kind is installed)
```bash
kind create cluster --name fastapi-cluster
```
```bash
kubectl cluster-info --context kind-fastapi-cluster
```

### Load Your Local Docker Image into Kind

Build the image locally:
```bash
docker build -t docker-s3-fastapi:latest .
```
Load it into Kind:
```bash
kind load docker-image docker-s3-fastapi:latest --name fastapi-cluster
```

### Install the Helm Chart
> 💡 **Best Practice:** Do not hardcode AWS credentials or sensitive values in Helm charts or Dockerfiles.  
> Use Kubernetes Secrets or AWS IAM Roles for Service Accounts (IRSA) when deploying in AWS EKS.


In the helm directory, run:
```bash
helm install docker-s3-fastapi ./docker-s3-fastapi \
  --set image.repository=docker-s3-fastapi \
  --set image.tag=latest \
  --set env.AWS_PROFILE=<profile> \
  --set env.S3_BUCKET=<s3_bucket> \
  --set env.AWS_REGION=<aws_region>
```

### Verify the Deployment
```bash
kubectl get pods
```
Check result (example output):
```
NAME                                 READY   STATUS    RESTARTS   AGE
docker-s3-fastapi-6fc45d7b57-77v6k   1/1     Running   0          5s
```
---
```bash
kubectl get svc
```

Check result (example output):
```
NAME                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
docker-s3-fastapi   ClusterIP   10.96.115.252   <none>        8080/TCP   20s
```

### (Optional) Port-forward for Local Access:
> ⚠️ Note: In this local Kind test without AWS integration, `/data` will not return S3 data — step shown for completeness.
```bash
kubectl port-forward svc/docker-s3-fastapi 8080:8080

```

### (Optional) Test:
```
http://localhost:8080/data
```

### Delete the Cluster
When done testing:
```bash
kind delete cluster --name fastapi-cluster
```

## 📜 License
MIT License – free for personal and commercial use, minimal restrictions.

## 📬 Contact

Author: **Lucjan Konopka**

LinkedIn: https://www.linkedin.com/in/lucjankonopka/

GitHub: https://github.com/lucjankonopka