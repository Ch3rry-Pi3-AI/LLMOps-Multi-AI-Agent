# 🐧 **Docker Setup on Ubuntu (WSL) — LLMOps Multi-AI Agent**

This branch explains how to install **Ubuntu via WSL**, then install the **Docker Engine inside Ubuntu**, and finally configure Docker so it can run **without sudo**.
This setup is required for containerisation workflows in later stages of the project.

## 🔧 Step 1: Enable WSL and Virtualisation

Open **PowerShell as Administrator** and run:

```powershell
wsl --install
```

If WSL is already installed, update it:

```powershell
wsl --update
```

Reboot your system if prompted.

## 🛍️ Step 2: Install Ubuntu (WSL)

1. Open **Microsoft Store**
2. Search for **Ubuntu**
3. Choose a version such as **Ubuntu 22.04 LTS**
4. Click **Get** / **Install**
5. Launch Ubuntu from the Start Menu
6. Create a **username** and **password** when prompted

## 🐳 Step 3: Install Docker Engine Inside Ubuntu

Official instructions:
[https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)

Scroll to **Install using the apt repository**.

### 3.1 Set up Docker’s apt repository

Run the following commands inside the **Ubuntu terminal**:

```bash
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

Add the Docker repository:

```bash
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF
```

Update package lists:

```bash
sudo apt update
```

### 3.2 Install Docker packages

```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 3.3 Verify installation

Run:

```bash
sudo docker run hello-world
```

Expected output:

```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
17eec7bbc9d7: Pull complete
Digest: sha256:f7931603f70e13dbd844253370742c4fc4202d290c80442b2e68706d8f33ce26
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

This confirms Docker Engine is installed.

## 👤 Step 4: Allow Docker to Run Without sudo

Docs:
[https://docs.docker.com/engine/install/linux-postinstall/](https://docs.docker.com/engine/install/linux-postinstall/)

Scroll to **Manage Docker as a non-root user**.

Run these in Ubuntu:

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

Verify:

```bash
docker run hello-world
```

If it prints the same **Hello from Docker!** message, your non-root setup is correct.

## 🔁 Step 5: Restart Terminal and Check Docker Version

Close Ubuntu, reopen it, then run:

```bash
docker version
```

Expected output example:

```
Client: Docker Engine - Community
 Version:           29.0.1
 API version:       1.52
 Go version:        go1.25.4
 Git commit:        eedd969
 Built:             Fri Nov 14 16:17:49 2025
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          29.0.1
  API version:      1.52 (minimum version 1.44)
  Go version:       go1.25.4
  Git commit:        198b5e3
  Built:             Fri Nov 14 16:17:49 2025
  OS/Arch:           linux/amd64
...
```

If you see both **Client** and **Server** sections, Docker is running correctly inside Ubuntu/WSL.

## ✅ Setup Complete

You now have:

* WSL enabled
* Ubuntu installed
* Docker Engine installed inside Ubuntu
* Docker working without sudo