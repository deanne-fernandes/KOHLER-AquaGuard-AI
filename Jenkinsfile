pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'areejrehan/aquaguard-ai'
        DOCKER_CREDENTIALS = credentials('dockerhub-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                sh 'python3 -m py_compile app.py'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$BUILD_NUMBER .'
            }
        }

        stage('Push Image') {
            steps {
                sh 'echo "$DOCKER_CREDENTIALS_PSW" | docker login -u "$DOCKER_CREDENTIALS_USR" --password-stdin'
                sh 'docker push $DOCKER_IMAGE:$BUILD_NUMBER'
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh "sed -i 's|image: areejrehan/aquaguard-ai:.*|image: areejrehan/aquaguard-ai:${BUILD_NUMBER}|' k8s/deployment.yaml"
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
                sh 'kubectl rollout status deployment/aquaguard-deployment --timeout=120s'
            }
        }

        stage('Verification') {
            steps {
                sh 'kubectl get pods'
                sh 'kubectl get deployments'
                sh 'kubectl get services'
            }
        }
    }
}
