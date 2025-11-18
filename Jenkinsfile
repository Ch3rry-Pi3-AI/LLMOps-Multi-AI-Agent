/*
Jenkinsfile
===========

CI/CD pipeline for the **LLMOps Multi-AI Agent** project.

This pipeline performs:

1. GitHub source checkout  
2. Static code analysis via **SonarQube**  
3. Docker image build + push to AWS Elastic Container Registry (ECR)  
4. Deployment trigger to **Amazon ECS Fargate**  

Credentials used:
* `github-token` (GitHub access token)
* `sonarqube-token` (SonarQube authentication)
* `aws-token` (AWS IAM access key with ECR/ECS permissions)

This pipeline is designed to run inside the **Jenkins DinD** container
configured earlier, allowing full Docker build capability.
*/


// ======================================================================
// Pipeline Setup
// ======================================================================
pipeline {
    agent any

    environment {
        // SonarQube configuration
        SONAR_PROJECT_KEY = 'LLMOPS'
        SONAR_SCANNER_HOME = tool 'Sonarqube'

        // AWS settings
        AWS_REGION = 'eu-west-2'
        ECR_REPO   = 'my-repo'
        IMAGE_TAG  = 'latest'
    }


// ======================================================================
// Pipeline Stages
// ======================================================================
    stages {

        // --------------------------------------------------------------
        // Stage 1: Clone source code from GitHub
        // --------------------------------------------------------------
        stage('Cloning GitHub Repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning GitHub repository into Jenkins workspace...'

                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',
                            url: 'https://github.com/Ch3rry-Pi3-AI/LLMOps-Multi-AI-Agent.git'
                        ]]
                    )
                }
            }
        }


        // --------------------------------------------------------------
        // Stage 2: Run SonarQube Static Analysis
        // --------------------------------------------------------------
        stage('SonarQube Analysis') {
            steps {
                withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {

                    withSonarQubeEnv('Sonarqube') {

                        sh """
                        ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                          -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                          -Dsonar.sources=. \
                          -Dsonar.host.url=http://sonarqube-dind:9000 \
                          -Dsonar.login=${SONAR_TOKEN}
                        """
                    }
                }
            }
        }


        // --------------------------------------------------------------
        // Stage 3: Build + Push Docker Image to AWS ECR
        // --------------------------------------------------------------
        stage('Build and Push Docker Image to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {

                        // Retrieve AWS account ID dynamically
                        def accountId = sh(
                            script: "aws sts get-caller-identity --query Account --output text",
                            returnStdout: true
                        ).trim()

                        def ecrUrl = "${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"

                        sh """
                        # Authenticate Docker to AWS ECR
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}

                        # Build Docker image
                        docker build -t ${ECR_REPO}:${IMAGE_TAG} .

                        # Tag the image for ECR
                        docker tag ${ECR_REPO}:${IMAGE_TAG} ${ecrUrl}:${IMAGE_TAG}

                        # Push the image to AWS ECR
                        docker push ${ecrUrl}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }


        // --------------------------------------------------------------
        // Stage 4: Deploy Updated Task to ECS Fargate
        // --------------------------------------------------------------
        stage('Deploy to ECS Fargate') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {

                        sh """
                        aws ecs update-service \
                          --cluster multi-ai-agent-cluster \
                          --service multi-ai-agent-def-service-95uyr1sp \
                          --force-new-deployment \
                          --region ${AWS_REGION}
                        """
                    }
                }
            }
        }

    } // end stages
}
