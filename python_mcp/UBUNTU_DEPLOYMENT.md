# Ubuntu 22.04 Deployment Guide for Python MCP HTTP Servers

Simple HTTP deployment for development and testing on Ubuntu 22.04 LTS.

## 📋 What You'll Get

- Python MCP servers running as systemd services
- Nginx reverse proxy for better management
- Basic firewall configuration
- Automatic restart on failure
- Centralized logging

**Note**: This is for development/internal use with HTTP. For production with public access, add SSL/TLS.

---

## Prerequisites

- Ubuntu 22.04 LTS server
- Root or sudo access
- Basic Linux command line knowledge

---

## Initial Server Setup

### 1. Update System Packages

```bash
# Update package list
sudo apt update

# Upgrade installed packages
sudo apt upgrade -y

# Install essential tools
sudo apt install -y curl wget git vim htop
```

### 2. Create Application User

```bash
# Create mcp user without login shell (security best practice)
sudo useradd -r -s /bin/false mcp
```

### 3. Configure System Limits

```bash
# Increase file descriptor limits
sudo tee -a /etc/security/limits.conf << EOF
mcp soft nofile 65536
mcp hard nofile 65536
EOF

# Apply immediately
sudo sysctl -w fs.file-max=65536
```

---

## Install Dependencies

### 1. Install Python

```bash
# Use system Python 3.10 (comes with Ubuntu 22.04)
sudo apt install -y python3 python3-venv python3-pip python3-dev

# Verify installation
python3 --version
```

### 2. Install System Dependencies

```bash
# Install build tools
sudo apt install -y build-essential libssl-dev libffi-dev

# Install additional dependencies for geopy and certifi
sudo apt install -y libgeos-dev libproj-dev ca-certificates
```

---

## Deploy Application

### 1. Create Application Directory

```bash
# Create app directory
sudo mkdir -p /opt/mcp-servers
sudo chown mcp:mcp /opt/mcp-servers

# Switch to mcp user (if you created it with shell)
sudo -u mcp bash

# Or stay as your user and use sudo for file operations
```

### 2. Upload Application Files

```bash
# From your local machine, upload files via SCP
scp calculator_server_http.py weather_server_http.py requirements.txt user@your-server:/tmp/

# On server, move files to app directory
sudo mkdir -p /opt/mcp-servers
sudo mv /tmp/calculator_server_http.py /opt/mcp-servers/
sudo mv /tmp/weather_server_http.py /opt/mcp-servers/
sudo mv /tmp/requirements.txt /opt/mcp-servers/
sudo chown -R mcp:mcp /opt/mcp-servers
```

### 3. Create Virtual Environment

```bash
# Create virtual environment
cd /opt/mcp-servers
sudo -u mcp python3 -m venv env

# Install dependencies
sudo -u mcp bash -c "source env/bin/activate && pip install --upgrade pip"
sudo -u mcp bash -c "source env/bin/activate && pip install -r requirements.txt"
```

### 4. Test Manual Run

```bash
# Test calculator server (Ctrl+C to stop after seeing output)
sudo -u mcp bash -c "cd /opt/mcp-servers && source env/bin/activate && python calculator_server_http.py"
```

---

## Configure systemd Services

### 1. Create Calculator Service

```bash
sudo tee /etc/systemd/system/mcp-calculator.service << 'EOF'
[Unit]
Description=MCP Calculator HTTP Server
After=network.target

[Service]
Type=simple
User=mcp
Group=mcp
WorkingDirectory=/opt/mcp-servers
Environment="PATH=/opt/mcp-servers/env/bin:/usr/bin"
ExecStart=/opt/mcp-servers/env/bin/python calculator_server_http.py

# Restart policy
Restart=always
RestartSec=10

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/mcp-servers

# Resource limits
LimitNOFILE=65536

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=mcp-calculator

[Install]
WantedBy=multi-user.target
EOF
```

### 2. Create Weather Service

```bash
sudo tee /etc/systemd/system/mcp-weather.service << 'EOF'
[Unit]
Description=MCP Weather HTTP Server
After=network.target

[Service]
Type=simple
User=mcp
Group=mcp
WorkingDirectory=/opt/mcp-servers
Environment="PATH=/opt/mcp-servers/env/bin:/usr/bin"
ExecStart=/opt/mcp-servers/env/bin/python weather_server_http.py

# Restart policy
Restart=always
RestartSec=10

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/mcp-servers

# Resource limits
LimitNOFILE=65536

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=mcp-weather

[Install]
WantedBy=multi-user.target
EOF
```

### 3. Enable and Start Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable services (start on boot)
sudo systemctl enable mcp-calculator.service
sudo systemctl enable mcp-weather.service

# Start services
sudo systemctl start mcp-calculator.service
sudo systemctl start mcp-weather.service

# Check status
sudo systemctl status mcp-calculator.service
sudo systemctl status mcp-weather.service

# View logs
sudo journalctl -u mcp-calculator.service -f
sudo journalctl -u mcp-weather.service -f
```

### 4. Verify Services Running

```bash
# Check both services are active
sudo systemctl status mcp-calculator.service mcp-weather.service

# Test endpoints
curl -N http://localhost:8000/sse
curl -N http://localhost:8001/sse
```

---

## Setup Nginx Reverse Proxy (Optional but Recommended)

### 1. Install Nginx

```bash
# Install Nginx
sudo apt install -y nginx

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Check status
sudo systemctl status nginx
```

### 2. Create Nginx Configuration

```bash
sudo tee /etc/nginx/sites-available/mcp-servers << 'EOF'
# Calculator Server
server {
    listen 80;
    server_name _;

    # Calculator endpoint
    location /calculator/sse {
        proxy_pass http://127.0.0.1:8000/sse;
        proxy_http_version 1.1;
        
        # SSE specific headers
        proxy_set_header Connection '';
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 86400s;
        
        # Standard proxy headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Calculator messages endpoint
    location /calculator/messages/ {
        proxy_pass http://127.0.0.1:8000/messages/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }

    # Weather endpoint
    location /weather/sse {
        proxy_pass http://127.0.0.1:8001/sse;
        proxy_http_version 1.1;
        
        # SSE specific headers
        proxy_set_header Connection '';
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 86400s;
        
        # Standard proxy headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Weather messages endpoint
    location /weather/messages/ {
        proxy_pass http://127.0.0.1:8001/messages/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
}
EOF
```

### 3. Enable Configuration

```bash
# Test Nginx configuration
sudo nginx -t

# Create symbolic link to enable site
sudo ln -s /etc/nginx/sites-available/mcp-servers /etc/nginx/sites-enabled/

# Remove default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Reload Nginx
sudo systemctl reload nginx
```

### 4. Test Reverse Proxy

```bash
# Test calculator endpoint
curl -N http://your-server-ip/calculator/sse

# Test weather endpoint
curl -N http://your-server-ip/weather/sse
```

---

## Firewall Configuration

```bash
# Enable UFW firewall
sudo ufw enable

# Allow SSH (IMPORTANT!)
sudo ufw allow 22/tcp

# Allow HTTP
sudo ufw allow 80/tcp

# Check status
sudo ufw status
```

---

## View Logs

```bash
# Service logs (real-time)
sudo journalctl -u mcp-calculator.service -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Check system resources
free -h
df -h
```

---

## Troubleshooting

```bash
# Check service status
sudo systemctl status mcp-calculator.service

# View logs
sudo journalctl -xeu mcp-calculator.service

# Restart service
sudo systemctl restart mcp-calculator.service

# Check if port is in use
sudo lsof -i :8000

# Test Nginx config
sudo nginx -t
```

---

## Security Hardening (Optional)

For internal/development use, basic security is sufficient. For production:

```bash
# Add basic authentication
sudo apt install -y apache2-utils
sudo htpasswd -c /etc/nginx/.htpasswd mcp_user

# Then add to Nginx location blocks:
# auth_basic "MCP Server";
# auth_basic_user_file /etc/nginx/.htpasswd;
```

---

## Quick Reference Commands

```bash
# Service management
sudo systemctl start mcp-calculator.service
sudo systemctl stop mcp-calculator.service
sudo systemctl restart mcp-calculator.service
sudo systemctl status mcp-calculator.service

# View logs
sudo journalctl -u mcp-calculator.service -f

# Test endpoints (direct)
curl -N http://localhost:8000/sse

# Test endpoints (via Nginx)
curl -N http://your-server-ip/calculator/sse
```

---

## Deployment Complete!

Your MCP servers are now running:

✅ Python servers running as systemd services
✅ Auto-restart on failure
✅ Firewall configured
✅ Nginx proxy (optional)

### Access URLs

**Direct access:**
- Calculator: `http://your-server-ip:8000/sse`
- Weather: `http://your-server-ip:8001/sse`

**Via Nginx** (if configured):
- Calculator: `http://your-server-ip/calculator/sse`
- Weather: `http://your-server-ip/weather/sse`

### Client Configuration

```json
{
  "mcpServers": {
    "calculator": {
      "url": "http://your-server-ip:8000/sse",
      "transport": "sse"
    },
    "weather": {
      "url": "http://your-server-ip:8001/sse",
      "transport": "sse"
    }
  }
}
```

You're all set! 🚀
