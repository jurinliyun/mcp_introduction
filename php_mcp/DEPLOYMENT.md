# PHP MCP Server - Production Deployment Guide

This guide provides step-by-step instructions for deploying the PHP MCP server in production environments on Windows (XAMPP) and Ubuntu 22.04+.

---

## 🪟 Windows Deployment (XAMPP)

### Prerequisites
- Windows 10/11 or Windows Server 2019+
- XAMPP 8.0+ installed ([Download here](https://www.apachefriends.org/download.html))
- Composer installed ([Download here](https://getcomposer.org/download/))

### Step 1: Install XAMPP

1. **Download and Install XAMPP**
   ```
   - Download XAMPP for Windows (PHP 8.0 or higher)
   - Run the installer
   - Install to: C:\xampp (recommended)
   - Select components: Apache, PHP (MySQL optional)
   ```

2. **Verify Installation**
   - Open XAMPP Control Panel
   - Start Apache
   - Open browser: http://localhost (should see XAMPP welcome page)

### Step 2: Install Composer

1. **Download Composer**
   - Download Composer-Setup.exe from getcomposer.org
   - Run installer (it will detect PHP from XAMPP)
   - Use PHP from: `C:\xampp\php\php.exe`

2. **Verify Composer**
   ```cmd
   composer --version
   ```

### Step 3: Deploy PHP MCP Application

1. **Copy Application Files**
   ```cmd
   # Create deployment directory
   mkdir C:\xampp\htdocs\php_mcp
   
   # Copy your files to:
   C:\xampp\htdocs\php_mcp\
   ```

2. **Install Dependencies**
   ```cmd
   cd C:\xampp\htdocs\php_mcp
   composer install --no-dev --optimize-autoloader
   ```

3. **Verify File Structure**
   ```
   C:\xampp\htdocs\php_mcp\
   ├── src/
   │   ├── CalculatorElements.php
   │   ├── CalculatorPrompt.php
   │   └── PayrollElements.php
   ├── vendor/
   ├── composer.json
   ├── mcp-http-server.php
   └── mcp-server.php
   ```

### Step 4: Configure PHP for Production

1. **Edit php.ini**
   - Open: `C:\xampp\php\php.ini`
   - Modify these settings:
   ```ini
   ; Production settings
   display_errors = Off
   log_errors = On
   error_log = "C:\xampp\php\logs\php_error.log"
   
   ; Memory and execution
   memory_limit = 256M
   max_execution_time = 300
   
   ; Enable required extensions
   extension=openssl
   extension=mbstring
   extension=curl
   ```

2. **Restart Apache**
   - In XAMPP Control Panel, click "Stop" then "Start" for Apache

### Step 5: Run MCP Server

**Option A: Run as Command Line Process (Recommended)**

1. **Create Startup Script** (`C:\xampp\htdocs\php_mcp\start-mcp-server.bat`)
   ```batch
   @echo off
   echo Starting PHP MCP HTTP Server...
   cd /d C:\xampp\htdocs\php_mcp
   C:\xampp\php\php.exe mcp-http-server.php
   ```

2. **Run the Server**
   ```cmd
   cd C:\xampp\htdocs\php_mcp
   start-mcp-server.bat
   ```

3. **Verify Server is Running**
   - Server should start on: http://127.0.0.1:8081/mcp
   - Check logs in console output

**Option B: Run as Windows Service (Advanced)**

1. **Install NSSM (Non-Sucking Service Manager)**
   - Download from: https://nssm.cc/download
   - Extract to: `C:\nssm`

2. **Create Service**
   ```cmd
   cd C:\nssm\win64
   nssm install PHPMCPServer "C:\xampp\php\php.exe" "C:\xampp\htdocs\php_mcp\mcp-http-server.php"
   nssm set PHPMCPServer AppDirectory "C:\xampp\htdocs\php_mcp"
   nssm set PHPMCPServer Description "PHP MCP HTTP Server"
   nssm set PHPMCPServer Start SERVICE_AUTO_START
   ```

3. **Start the Service**
   ```cmd
   nssm start PHPMCPServer
   ```

4. **Verify Service**
   ```cmd
   nssm status PHPMCPServer
   ```

### Step 6: Configure Firewall

1. **Open Windows Firewall**
   - Search for "Windows Defender Firewall"
   - Click "Advanced settings"

2. **Create Inbound Rule**
   - Click "Inbound Rules" → "New Rule"
   - Rule Type: Port
   - Protocol: TCP
   - Port: 8081
   - Action: Allow the connection
   - Profile: Select appropriate (Domain/Private/Public)
   - Name: "PHP MCP Server"

### Step 7: Production Configuration

1. **Edit Server Configuration**
   - Open: `mcp-http-server.php`
   - Modify for production:
   ```php
   // Change host if needed (keep 127.0.0.1 per MCP protocol)
   $transport = new StreamableHttpServerTransport(
       host: '127.0.0.1',  // MCP protocol requires this
       port: 8081,
       mcpPath: '/mcp',
       enableJsonResponse: false,
       stateless: false
   );
   ```

2. **Setup Reverse Proxy (Optional)**
   - If you need external access, use Apache as reverse proxy
   - Edit: `C:\xampp\apache\conf\httpd.conf`
   - Enable modules:
   ```apache
   LoadModule proxy_module modules/mod_proxy.so
   LoadModule proxy_http_module modules/mod_proxy_http.so
   ```
   - Add virtual host configuration (see section below)

---

## 🐧 Ubuntu 22.04+ Deployment

### Prerequisites
- Ubuntu 22.04 LTS or higher
- Root or sudo access
- Internet connection

### Step 1: Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install Apache and PHP

1. **Install Apache**
   ```bash
   sudo apt install apache2 -y
   sudo systemctl enable apache2
   sudo systemctl start apache2
   ```

2. **Install PHP 8.1+ and Extensions**
   ```bash
   sudo apt install php8.1 php8.1-cli php8.1-common php8.1-curl php8.1-mbstring php8.1-xml php8.1-zip -y
   ```

3. **Verify Installation**
   ```bash
   php -v
   apache2 -v
   ```

### Step 3: Install Composer

```bash
# Download installer
curl -sS https://getcomposer.org/installer -o composer-setup.php

# Verify installer (optional but recommended)
HASH=$(curl -sS https://composer.github.io/installer.sig)
php -r "if (hash_file('SHA384', 'composer-setup.php') === '$HASH') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"

# Install globally
sudo php composer-setup.php --install-dir=/usr/local/bin --filename=composer

# Clean up
rm composer-setup.php

# Verify
composer --version
```

### Step 4: Deploy Application

1. **Create Application Directory**
   ```bash
   sudo mkdir -p /var/www/php_mcp
   sudo chown -R $USER:www-data /var/www/php_mcp
   cd /var/www/php_mcp
   ```

2. **Copy Application Files**
   ```bash
   # Upload your files to /var/www/php_mcp
   # You can use scp, rsync, or git
   
   # Example with git:
   # git clone <your-repo> /var/www/php_mcp
   
   # Or manually copy files
   # Ensure this structure:
   # /var/www/php_mcp/
   # ├── src/
   # ├── composer.json
   # └── mcp-http-server.php
   ```

3. **Install Dependencies**
   ```bash
   cd /var/www/php_mcp
   composer install --no-dev --optimize-autoloader
   ```

4. **Set Permissions**
   ```bash
   sudo chown -R www-data:www-data /var/www/php_mcp
   sudo chmod -R 755 /var/www/php_mcp
   ```

### Step 5: Create Systemd Service

1. **Create Service File**
   ```bash
   sudo nano /etc/systemd/system/php-mcp-server.service
   ```

2. **Add Service Configuration**
   ```ini
   [Unit]
   Description=PHP MCP HTTP Server
   After=network.target
   
   [Service]
   Type=simple
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/php_mcp
   ExecStart=/usr/bin/php /var/www/php_mcp/mcp-http-server.php
   Restart=always
   RestartSec=10
   StandardOutput=journal
   StandardError=journal
   
   # Security settings
   NoNewPrivileges=true
   PrivateTmp=true
   ProtectSystem=strict
   ProtectHome=true
   ReadWritePaths=/var/www/php_mcp
   
   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable php-mcp-server
   sudo systemctl start php-mcp-server
   ```

4. **Check Service Status**
   ```bash
   sudo systemctl status php-mcp-server
   ```

5. **View Logs**
   ```bash
   sudo journalctl -u php-mcp-server -f
   ```

### Step 6: Configure Firewall

```bash
# Allow SSH (if not already allowed)
sudo ufw allow 22/tcp

# Allow Apache (if serving web content)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow MCP server port (if external access needed)
sudo ufw allow 8081/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### Step 7: Production Configuration

1. **Configure PHP for Production**
   ```bash
   sudo nano /etc/php/8.1/cli/php.ini
   ```
   
   Modify:
   ```ini
   display_errors = Off
   log_errors = On
   error_log = /var/log/php/mcp-error.log
   memory_limit = 256M
   max_execution_time = 300
   ```

2. **Create Log Directory**
   ```bash
   sudo mkdir -p /var/log/php
   sudo chown www-data:www-data /var/log/php
   ```

3. **Setup Log Rotation**
   ```bash
   sudo nano /etc/logrotate.d/php-mcp-server
   ```
   
   Add:
   ```
   /var/log/php/*.log {
       daily
       missingok
       rotate 14
       compress
       delaycompress
       notifempty
       create 0640 www-data www-data
       sharedscripts
   }
   ```

### Step 8: Setup Reverse Proxy (Optional)

If you need to expose the MCP server through Apache:

1. **Enable Apache Modules**
   ```bash
   sudo a2enmod proxy
   sudo a2enmod proxy_http
   sudo a2enmod headers
   ```

2. **Create Virtual Host**
   ```bash
   sudo nano /etc/apache2/sites-available/mcp-server.conf
   ```
   
   Add:
   ```apache
   <VirtualHost *:80>
       ServerName mcp.yourdomain.com
       
       ProxyPreserveHost On
       ProxyPass / http://127.0.0.1:8081/
       ProxyPassReverse / http://127.0.0.1:8081/
       
       # Security headers
       Header always set X-Content-Type-Options "nosniff"
       Header always set X-Frame-Options "DENY"
       
       ErrorLog ${APACHE_LOG_DIR}/mcp-error.log
       CustomLog ${APACHE_LOG_DIR}/mcp-access.log combined
   </VirtualHost>
   ```

3. **Enable Site and Restart Apache**
   ```bash
   sudo a2ensite mcp-server.conf
   sudo systemctl restart apache2
   ```

---

## 🔍 Testing the Deployment

### Test MCP Server Endpoint

**Windows:**
```cmd
curl http://127.0.0.1:8081/mcp
```

**Ubuntu:**
```bash
curl http://127.0.0.1:8081/mcp
```

### Test from Claude Desktop

Add to your Claude Desktop config:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS/Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "php-calculator": {
      "url": "http://127.0.0.1:8081/mcp"
    }
  }
}
```

---

## 🛠️ Troubleshooting

### Windows Issues

**Issue: Port 8081 already in use**
```cmd
netstat -ano | findstr :8081
taskkill /PID <PID> /F
```

**Issue: PHP not found**
- Add PHP to PATH: `C:\xampp\php`
- Or use full path in scripts

**Issue: Service won't start**
```cmd
nssm status PHPMCPServer
nssm edit PHPMCPServer
```

### Ubuntu Issues

**Issue: Service fails to start**
```bash
sudo journalctl -u php-mcp-server -n 50 --no-pager
```

**Issue: Permission denied**
```bash
sudo chown -R www-data:www-data /var/www/php_mcp
sudo chmod -R 755 /var/www/php_mcp
```

**Issue: Port already in use**
```bash
sudo lsof -i :8081
sudo kill <PID>
```

**Issue: PHP extensions missing**
```bash
php -m | grep -E 'mbstring|curl|openssl'
sudo apt install php8.1-<extension>
```

---

## 🔒 Security Best Practices

1. **Network Security**
   - Keep MCP server bound to 127.0.0.1 (per MCP protocol)
   - Use reverse proxy for external access
   - Enable HTTPS with SSL certificates
   - Use firewall to restrict access

2. **Application Security**
   - Disable display_errors in production
   - Keep Composer dependencies updated
   - Use environment variables for sensitive config
   - Implement rate limiting

3. **System Security**
   - Keep OS and packages updated
   - Use non-root user for service
   - Enable SELinux/AppArmor (Ubuntu)
   - Regular security audits

---

## 📊 Monitoring

### Windows
- Use Windows Event Viewer
- Monitor service status with Task Manager
- Setup external monitoring tools

### Ubuntu
```bash
# Service status
sudo systemctl status php-mcp-server

# Live logs
sudo journalctl -u php-mcp-server -f

# Resource usage
htop
ps aux | grep php

# Port status
sudo netstat -tlnp | grep 8081
```

---

## 🔄 Maintenance

### Update Application

**Windows:**
```cmd
cd C:\xampp\htdocs\php_mcp
composer update --no-dev --optimize-autoloader
# Restart service or process
```

**Ubuntu:**
```bash
cd /var/www/php_mcp
composer update --no-dev --optimize-autoloader
sudo systemctl restart php-mcp-server
```

### Backup

**Windows:**
```cmd
xcopy C:\xampp\htdocs\php_mcp C:\backups\php_mcp_%DATE% /E /I /H
```

**Ubuntu:**
```bash
sudo tar -czf /backup/php_mcp_$(date +%Y%m%d).tar.gz /var/www/php_mcp
```

---

## 📞 Support

For issues specific to:
- **PHP MCP Library**: https://github.com/php-mcp/server
- **XAMPP**: https://www.apachefriends.org/support.html
- **Apache**: https://httpd.apache.org/docs/

---

## ✅ Production Checklist

- [ ] PHP 8.1+ installed and configured
- [ ] Composer dependencies installed
- [ ] Server runs on 127.0.0.1:8081
- [ ] Service/process auto-starts on boot
- [ ] Firewall configured properly
- [ ] Logs rotating and monitored
- [ ] Backup strategy in place
- [ ] Security headers configured
- [ ] Error handling and logging enabled
- [ ] Health check monitoring setup
