# ======================================================================
# Base Image
# ======================================================================
FROM jenkins/jenkins:lts

# ======================================================================
# Switch to Root for System-Level Installation
# ======================================================================
USER root

# ======================================================================
# Install Docker Engine Inside the Jenkins Container
# ======================================================================
# 1. Install minimal dependencies (ca-certificates, curl, gnupg).
# 2. Add Docker's official GPG key and repository.
# 3. Install Docker Engine components.
RUN apt-get update -y && \
    apt-get install -y ca-certificates curl gnupg && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean

# ======================================================================
# Configure Docker Group Access for Jenkins User
# ======================================================================
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# ======================================================================
# Docker Storage Directory
# ======================================================================
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# ======================================================================
# Return to Jenkins User Context
# ======================================================================
USER jenkins
