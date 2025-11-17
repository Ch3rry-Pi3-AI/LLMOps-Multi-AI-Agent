# ======================================================================
# Base Image
# ======================================================================
# Start from the official Jenkins LTS image.
# This provides a stable, production-grade Jenkins controller.
FROM jenkins/jenkins:lts


# ======================================================================
# Switch to Root for System-Level Installation
# ======================================================================
# Jenkins runs as user "jenkins" by default, but installing Docker
# requires root privileges. After installation, we will switch back.
USER root


# ======================================================================
# Install Docker Engine Inside the Jenkins Container
# ======================================================================
# Steps:
#   1. Install required packages for Docker repository handling.
#   2. Add Docker’s official Debian GPG key.
#   3. Add Docker repository to apt sources list.
#   4. Install Docker Engine components (docker-ce, cli, containerd).
#   5. Clean apt cache to reduce image size.
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean


# ======================================================================
# Configure Docker Group Access for Jenkins User
# ======================================================================
# Create the docker group if it doesn't already exist (idempotent),
# then add the Jenkins user to it. This allows Jenkins pipelines to run
# docker build / docker run commands without root privileges.
RUN groupadd -f docker && \
    usermod -aG docker jenkins


# ======================================================================
# Docker Storage Directory
# ======================================================================
# Create Docker's default storage directory.
# Declaring it as a volume ensures persistency and compatibility for
# Docker-in-Docker (DinD) operations inside Jenkins pipelines.
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker


# ======================================================================
# Return to Jenkins User Context
# ======================================================================
# After installing system packages and configuring permissions, switch back
# to the Jenkins user as recommended for security and Jenkins operations.
USER jenkins
