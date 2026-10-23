# KOHLER AquaGuard AI – DevOps CI/CD Pipeline

## Project Overview

KOHLER AquaGuard AI is a Streamlit-based application developed using Python and Pandas. The application uses sensor data stored in a CSV file and provides a dashboard for monitoring water-related information.

For this DevOps project, an automated CI/CD pipeline was created using Jenkins, Docker, Docker Hub, Kubernetes, Minikube, GitHub, and AWS EC2.

The main purpose of the pipeline is to automatically fetch the latest source code, check the application, build a Docker image, push the image to Docker Hub, deploy the application on Kubernetes using Minikube, and verify the deployment.

## Technologies Used

- Python
- Streamlit
- Pandas
- Git and GitHub
- Jenkins
- Docker
- Docker Hub
- Kubernetes
- Minikube
- AWS EC2
- Ubuntu

## CI/CD Workflow

The implemented workflow is:

GitHub → Jenkins → Build/Test → Docker Build → Docker Hub → Kubernetes/Minikube → Application Verification

The Jenkins pipeline is defined using a `Jenkinsfile` stored in the GitHub repository.

## Pipeline Stages

### 1. Checkout

Jenkins retrieves the latest source code from the GitHub repository.

### 2. Build and Test

The application is checked using Python compilation:

`python3 -m py_compile app.py`

This verifies that the Python source file does not contain syntax errors.

### 3. Docker Build

Jenkins automatically builds a Docker image of the application using the `Dockerfile`.

Each Jenkins build uses its build number as the Docker image tag.

Example:

`areejrehan/aquaguard-ai:2`

### 4. Push Image to Docker Hub

After the image is successfully built, Jenkins authenticates with Docker Hub using credentials stored securely in Jenkins.

The newly created Docker image is then pushed to the Docker Hub repository.

### 5. Deploy to Kubernetes

Minikube is used to run a local Kubernetes cluster on the AWS EC2 instance.

The project contains two Kubernetes manifest files:

- `k8s/deployment.yaml`
- `k8s/service.yaml`

Jenkins applies these manifests and deploys the new Docker image to Kubernetes.

### 6. Verification

The pipeline verifies the Kubernetes deployment using commands such as:

`kubectl get pods`

`kubectl get deployments`

`kubectl get services`

The application is exposed through a Kubernetes Service and was successfully accessed through port 8501.

## AWS and Jenkins Setup

An Ubuntu EC2 instance was created on AWS and used as the DevOps server.

Jenkins, Docker, kubectl, and Minikube were installed and configured on this instance.

Jenkins was given permission to communicate with Docker and the Minikube Kubernetes cluster. Jenkins was then connected to the GitHub repository using a Pipeline job.

## Dockerization

A `Dockerfile` was created for the Streamlit application.

The Docker image:

- Uses Python 3.12 slim as the base image
- Installs dependencies from `requirements.txt`
- Copies the application files into the container
- Exposes port 8501
- Starts the Streamlit application

The image was successfully built and pushed to Docker Hub.

## Kubernetes Deployment

The application was deployed to Minikube using Kubernetes.

The Deployment manages the AquaGuard application pod, while the Service exposes the application on the required port.

The deployment was verified by checking the pod, deployment, and service status.

## CI/CD Update Demonstration

After the first successful pipeline execution, the application source code was modified.

The application title was changed to:

`KOHLER AquaGuard AI - Version 2`

The modified code was committed to GitHub and the Jenkins pipeline was executed again.

Jenkins automatically:

1. Retrieved the updated source code.
2. Performed the syntax check.
3. Built a new Docker image.
4. Pushed the new image to Docker Hub.
5. Updated the Kubernetes deployment.
6. Verified the running Kubernetes resources.

The second deployment completed successfully, and the updated Version 2 application was verified in the browser.

## Repository Structure

```text
KOHLER-AquaGuard-AI/
├── data/
│   └── sensor_data.csv
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── app.py
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
└── README.md
```

## Result

A complete CI/CD pipeline was successfully implemented for the KOHLER AquaGuard AI project. Jenkins automated the process from source-code retrieval through Docker image creation and registry push to Kubernetes deployment and verification.

The successful redeployment of Version 2 demonstrated that changes made to the application can be delivered through the same CI/CD workflow.
