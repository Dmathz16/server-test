# Server Test

For setting up production server with flask+nginx+gunicorn



## After running new instance in AWS EC2

**Connect to server using SSH in your terminal**
```cmd
ssh -i <path_to_pem_file> ubuntu@<ipaddress>
```

**Update ubuntu software**
```cmd
sudo apt update
```

1. **Install and enable web server (nginx)**
   
   ```cmd
   sudo apt install nginx -y
   ```
   ```cmd
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```


3. **Set server account**
   
   * Change root password
      ```cmd
      sudo passwd root
      ```
   
   * Add new user
     
      ```cmd
      sudo -i
      ```
      ```cmd
      adduser <new-user>
      ```
      
      * Add user to sudo group
         ```cmd
         usermod -aG sudo <new-user>
         ```
         
      * Add user to www-data group and set permission
         ```cmd
         usermod -aG www-data <new-user>
         sudo chmod -R 775 /var/www
         sudo chown -R <new-user>:www-data /var/www
         ```
         
      * Open sshd_config file
         ```cmd
         nano /etc/ssh/sshd_config
         ```
     
      * Uncomment code like this then save
         ```cmd
         PasswordAuthentication yes
         ```
     
      * Restart ssh service
         ```cmd
         sudo systemctl restart ssh.service
         ```
     
      * Set new user ssh access 
         ```cmd
         sudo mkdir -p /home/<new-user>/.ssh
         sudo chmod 700 /home/<new-user>/.ssh
         sudo cp /home/<old-user>/.ssh/authorized_keys /home/<new-user>/.ssh/authorized_keys
         ```
         
         ```cmd
         sudo chmod 600 /home/<new-user>/.ssh/authorized_keys
         sudo chown -R <new-user>:<new-user> /home/<new-user>/.ssh
         ```
      
   * Remove default user named **ubuntu**
      * Show processes running under ubuntu
         ```cmd
         ps -u ubuntu
         ```
     
      * Kill process one by one with PID(Process ID) using this
         ```cmd
         sudo kill <PID>
         ```
     
      * Remove **ubuntu** user if all processes has been killed
         ```cmd
         sudo userdel -r ubuntu
         ```
     
      * Exit root session
         ```cmd
         exit
         ```

   
4. **Set MySQL server** (If needed)
   * Install and setup server
      ```cmd
      sudo apt-get install mysql-server
      sudo mysql_secure_installation
      sudo systemctl status mysql
      ```
   
   * Connect to MySQL server
      ```cmd
      sudo mysql -u root -p
      ```
   
   * Create database
      ```cmd
      CREATE DATABASE <db_name>;
      SHOW DATABASES;
      EXIT;
      ```
   
   * Import existing sql
      ```cmd
      sudo mysql -u root -p <db_name> < <path_to_sql_file>
      ```
   
   * Check if data are imported
      ```cmd
      sudo mysql -u root -p
      SHOW DATABASES;
      USE <db_name>;
      SELECT * FROM <table_name>;
      EXIT;
      ```


5. **Set flask app**

   * Change directory
      ```cmd
      cd /var/www
      ```
   
   * Install requirements
      ```cmd
      sudo apt install python3-pip python3-venv git -y
      ```
   
   * Clone project from git
      ```cmd
      git clone <repository-url> <project-name>
      ```

   * Setup
      ```cmd
      cd <project-name>
      python3 -m venv .venv
      . .venv/bin/activate
      pip3 install flask
      pip3 install -r requirements.txt
      ```

   * Run app
      ```cmd
      python <app>.py
      ```
      or
      ```cmd
      flask --app <app> run
      ```

      
6. **Run with gunicorn + wsgi**
   
      Stop running app by pressing **ctrl + c**

   * Install gunicorn
      ```cmd
      pip3 install gunicorn
      ```

   * Run app with gunicorn
      ```cmd
      gunicorn --bind 0.0.0.0:5000 <app>:app
      ```

   * Stop gunicorn by pressing **ctrl + c** then create wsgi.py inside project directory
      ```cmd
      sudo nano /var/www/<project-name>/wsgi.py
      ```

   * Then paste this inside wsgi.py and save
      ```cmd
      from <app> import app
      
      if __name__ == '__main__':
      	app.run(host='0.0.0.0')
      ```

   * Run app with gunicorn + wsgi
      ```cmd
      gunicorn --bind 0.0.0.0:5000 wsgi:app
      ```

   * Deactivate environment if done testing
      ```cmd
      deactivate
      ```
   
   
7. **Run flask app in system service**
    
   * After deactivating python environment, create new service file
      ```cmd
      sudo nano /etc/systmd/system/<project-name>.service
      ```

   * Paste, update code then save this in service file
      ```cmd
      [Unit]
      Description=My app description
      After=network.target
      
      [Service]
      User=<username> 
      Group=www-data
      WorkingDirectory=/var/www/<project-name>
      Environment="PATH=/var/www/<project-name>/.venv/bin"
      ExecStart=/var/www/<project-name>/.venv/bin/gunicorn --workers 3 --bind unix:application.sock -m 007 wsgi:app
      
      # Log output configuration
      StandardOutput=append:/var/log/<project-name>/gunicorn_access.log
      StandardError=append:/var/log/<project-name>/gunicorn_error.log
      
      [Install]
      WantedBy=multi-user.target
      ```

   * Make directory for app logs
      ```cmd
      sudo mkdir -p /var/log/<project-name>
      ```

   * Set permission for that directory
      ```cmd
      sudo chown www-data:www-data /var/log/<project-name>
      ```

   * Start and enable new service
      ```cmd
      sudo systemctl daemon-reload
      sudo systemctl start <service-name>
      sudo systemctl enable <service-name>
      sudo systemctl status <service-name>
      ```

   * Check app logs
      ```cmd
      sudo tail -f /var/log/<project-name>/gunicorn_error.log
      ```


8. **Set nginc config** (with Domain name)

   * Check app logs
      ```cmd
      sudo nano /etc/nginx/sites-available/<project-name>.conf
      ```

   * Check app logs
      ```cmd
      # Redirect www.<domain_name> to <domain_name>
      server {
          listen 80;
          server_name www.<domain_name>;
      
          return 301 http://<domain_name>$request_uri;
      }
      # Redirect any IP address requests to <domain_name>
      server {
          listen 80;
          server_name <public_ip>;  
      
          return 301 http://<domain_name>$request_uri;
      }
      # Main server block for <domain_name>
      server {
          listen 80;
          server_name <domain_name>;
      
          location / {
              include proxy_params;
              proxy_pass http://unix:/var/www/<project-name>/application.sock;
          }
      }
      ```
      or if has ssl
      ``` cmd
      # Redirect www.<domain_name> to <domain_name>
      server {
          listen 80;
          server_name www.<domain_name>;
      
          return 301 http://<domain_name>$request_uri;
      }
      
      # Redirect any IP address requests to <domain_name>
      server {
          listen 80;
          server_name 54.255.58.113;
      
          return 301 http://<domain_name>$request_uri;
      }
      
      # Main block for domain (HTTP -> HTTPS redirection)
      server {
          listen 80;
          server_name <domain_name>;
      
          # Redirect HTTP to HTTPS
          return 301 https://$host$request_uri;
      }
      # Main server block for dmathz.com
      server {
      
          listen 443 ssl;
          server_name <domain_name>;
      
          # SSL Configuration
          ssl_certificate /etc/ssl/certs/<domain_name>/<cert>.crt;
          ssl_certificate_key /etc/ssl/certs/<domain_name>/<key>.key;
          ssl_trusted_certificate /etc/ssl/certs/<domain_name>/<bundle>.crt;
      
          # SSL Settings
          ssl_protocols TLSv1.2 TLSv1.3;
          ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
          ssl_prefer_server_ciphers on;
      
          location / {
              include proxy_params;
              proxy_pass http://unix:/var/www/<project-name>/application.sock;
          }
      }
      ```

   * Enable config
      ```cmd
      sudo ln -s /etc/nginx/sites-available/<project-name>.conf /etc/nginx/sites-enabled/
      ```

   * Check config error
      ```cmd
      sudo nginx -t
      ```

   * Restart nginx
      ```cmd
      sudo systemctl restart nginx
      ```

9. **Set firewall**

    * Enable firewall
      ```cmd
      sudo ufw enable
      ```

    * Allow port 80, 443 and 22(ssh)
      ```cmd
      sudo ufw allow "Nginx Full"
      sudo ufw allow ssh
      ```

    * Check status
      ```cmd
      sudo ufw status
      ```

10. **Set SSL**

    * On your local machine, open terminal to send ssl cert files using scp
      ```cmd
      scp -i <path_to_pem_file> <path_to_ssl_cert_file> ubuntu@<ipaddress>:/var/www
      ```

    * Install openssl to generate private key
      ```cmd
      sudo apt install openssl
      ```
   
    * Create directory for certificate files
      ```cmd
      sudo mkdir -p /etc/ssl/certs/<domain_name>
      ```

    * Generate **private key** without pass phrase
      ```cmd
      openssl genpkey -algorithm RSA -out <ssl_path>/dmathz.com.key
      ```

      **Including pass phrase increases security**

    * Generate CSR 
      ```cmd
      openssl req -new -key <ssl_path>/dmathz.com.key -out <ssl_path>/dmathz.com.csr
      ```

    * Open csr
      ```cmd
      sudo nano <ssl_path>/dmathz.com.csr
      ```
      
      **Copy the texts in .csr, it will be used to generate ssl from ssl providers (e.g. GoDaddy)**

    * After generating and downloading ssl certs, **in your computer**, send the certs one by one using SCP
      ```cmd
      scp -i <path_to_pem_file> <path_to_ssl_cert_file> ubuntu@<ipaddress>:/var/www
      ```

    * **In server**, move certs to directory
      ```cmd
      sudo mv <path_to_ssl_file> /etc/ssl/certs/<domain_name>/
      ```
      
    * Directory permission 
      ```cmd
      sudo chmod 600 /etc/ssl/certs/<domain_name>/*
      ```
   
    * Check changes 
      ```cmd
      sudo nginx -t
      ```
   
    * Reload nginx so that changes takes effect
      ```cmd
      sudo systemctl reload nginx
      ```


12. Project permission

      ```cmd
      sudo chmod 775 /var/www/<project-name>
      ```
