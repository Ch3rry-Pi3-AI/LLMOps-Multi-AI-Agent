# ⚙️ **Custom Jenkins Image — LLMOps Multi-AI Agent**

This folder contains a **custom Jenkins Docker image** designed specifically for CI/CD workflows that require **Docker-in-Docker (DinD)** capabilities.
This setup enables Jenkins pipelines to build, tag, run, and push Docker images directly from within Jenkins itself.

The image extends the official **`jenkins/jenkins:lts`** base image and installs the full Docker Engine, ensuring seamless integration with containerisation workflows across the Multi-AI Agent project.

## 📁 **Folder Contents**

```text
custom_jenkins/
└── Dockerfile        # Custom Jenkins image with Docker Engine installed
```

## 🧩 **Purpose of This Custom Image**

The default Jenkins LTS image does **not** include Docker.
For any CI/CD pipeline that needs to:

* Build Docker images
* Push images to DockerHub, GCP Artifact Registry, or ECR
* Run containers for testing
* Trigger containerised deployment workflows

Jenkins must have **local Docker Engine access**.

This custom image provides exactly that.

## 🔧 **What This Dockerfile Does**

The custom Jenkins image includes:

* Installation of Docker Engine (`docker-ce`, `docker-ce-cli`, `containerd.io`)
* Configuration of Docker’s Debian repository
* Creation of the `docker` group
* Adding Jenkins user (`jenkins`) to the `docker` group
  → Enables `docker build`, `docker run`, and `docker push` **without root**
* Creation of `/var/lib/docker` and declaration as a Docker volume
  → Required for Docker-in-Docker
* Return to Jenkins user for safe execution

This makes the Jenkins instance fully capable of handling container-based CI/CD workflows out of the box.

## 🚀 **How to Build and Run the Custom Jenkins Image**

### 1️⃣ Build the image

```bash
docker build -t custom-jenkins-docker ./custom_jenkins
```

### 2️⃣ Run Jenkins with proper permissions and volumes

```bash
docker run -d \
  --name jenkins-docker \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  custom-jenkins-docker
```

### Why mount the Docker socket?

Mounting:

```bash
-v /var/run/docker.sock:/var/run/docker.sock
```

allows the Jenkins container to talk to the **host’s Docker daemon**, which is the recommended method for secure and stable Docker builds.

## 🛠️ **When Should You Use This Image?**

You should use this custom Jenkins image when your pipeline needs:

* Docker builds
* Docker-based deployments
* Kubernetes workflows
* CI/CD with GCP Artifact Registry
* Jenkins → Docker → Kubernetes workflows
* Automated container publishing

If your pipeline uses Docker in *any* stage, this is the image you run Jenkins with.
