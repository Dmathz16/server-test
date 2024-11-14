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
      sudo apt-get install mysql-server -y
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

      ```cmd
      CREATE USER '<username>'@'localhost' IDENTIFIED BY '<password>';
      GRANT ALL PRIVILEGES ON <db_name>.* TO '<username>'@'localhost';
      FLUSH PRIVILEGES;
      EXIT;
      ```

   * For dump privilege (if needed)
      ```cmd
      GRANT PROCESS ON *.* TO 'rogin'@'localhost';
      FLUSH PRIVILEGES;
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

   * Open mysql config file
     ``` cmd
     sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
     ```

   * Open mysql config file
     ``` cmd
     [mysqld]
     thread_cache_size = 4
     innodb_thread_concurrency = 4
     innodb_read_io_threads = 2
     innodb_write_io_threads = 2
     wait_timeout = 300
     interactive_timeout = 300
     innodb_buffer_pool_size = 128M
     event_scheduler = OFF

     key_buffer              = 8M 
     max_connections         = 10 # Limit connections
     query_cache_size        = 8M # try 4m if not enough 
     query_cache_limit       = 512K
     thread_stack            = 128K

     performance_schema = 0
     ```
     
   * Dump mysql
     ``` cmd
     sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
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
      sudo nano /etc/systemd/system/<project-name>.service
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
      ExecStart=/var/www/<project-name>/.venv/bin/gunicorn --workers 2 --timeout 20 --bind unix:application.sock -m 007 wsgi:app
      
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
      
      server {
          listen 443 ssl;
          server_name www.<domain_name>;
      
          # SSL Configuration
          ssl_certificate /etc/ssl/certs/<domain_name>/<cert>.crt;
          ssl_certificate_key /etc/ssl/certs/<domain_name>/<key>.key;
          ssl_trusted_certificate /etc/ssl/certs/<domain_name>/<bundle>.crt;
      
          # SSL Settings
          ssl_protocols TLSv1.2 TLSv1.3;
          ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
          ssl_prefer_server_ciphers on;
      
          return 301 https://<domain_name>$request_uri;
      }
      
      # Redirect any IP address requests to <domain_name>
      server {
          listen 80;
          server_name 54.255.58.113;  # Replace with your actual IP address
      
          return 301 http://<domain_name>$request_uri;
      }
      
      server {
          listen 443 ssl;
          server_name 54.255.58.113;  # Replace with your actual IP address
      
          # SSL Configuration
          ssl_certificate /etc/ssl/certs/<domain_name>/<cert>.crt;
          ssl_certificate_key /etc/ssl/certs/<domain_name>/<key>.key;
          ssl_trusted_certificate /etc/ssl/certs/<domain_name>/<bundle>.crt;
      
          # SSL Settings
          ssl_protocols TLSv1.2 TLSv1.3;
          ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
          ssl_prefer_server_ciphers on;
      
          return 301 https://<domain_name>$request_uri;
      }
      
      # Main block for domain (HTTP -> HTTPS redirection)
      server {
          listen 80;
          server_name <domain_name>;
      
          # Redirect HTTP to HTTPS
          return 301 https://$host$request_uri;
      }
      
      # Main server block for <domain_name>
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

      ```cmd
      sudo ufw allow ssh
      sudo ufw allow 'Nginx Full'
      sudo ufw enable
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
      sudo openssl genpkey -algorithm RSA -out <ssl_path>/dmathz.com.key
      ```

      **Including pass phrase increases security**

    * Generate CSR 
      ```cmd
      sudo openssl req -new -key <ssl_path>/dmathz.com.key -out <ssl_path>/dmathz.com.csr
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


11. **Backup MySQL with AWS S3 and on your machine**

    * Create directories to store mysql dumps
      ```cmd
      sudo mkdir /var/backups/mysql 
      sudo mkdir /var/backups/mysql/minutely/
      sudo mkdir /var/backups/mysql/hourly/
      sudo mkdir /var/backups/mysql/daily/
      sudo mkdir /var/backups/mysql/weekly/
      sudo mkdir /var/backups/mysql/monthly/
      ```

    * Allow user as owner to that dirs
      ```cmd
      sudo chown <username>:<username> /var/backups/mysql
      sudo chown <username>:<username> /var/backups/mysql/minutely/
      sudo chown <username>:<username> /var/backups/mysql/hourly/
      sudo chown <username>:<username> /var/backups/mysql/daily/
      sudo chown <username>:<username> /var/backups/mysql/weekly/
      sudo chown <username>:<username> /var/backups/mysql/monthly/
      ```
      
    * Install AWS CLI
      ```cmd
      sudo apt install curl unzip
      curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
      unzip awscliv2.zip
      sudo ./aws/install
      aws --version
      ```

    * Setup S3 Bucket configurations
      ```cmd
      aws configure
      ```
      Go to AWS **S3** and **IAM** to get **credentials**

    * Check if S3 Bucket is available
      ```cmd
      aws s3 ls s3://<bucket_name>
      ```

    * Create directory for software **Cronjobs** (if didn't exist)
      ```cmd
      sudo mkdir -p /usr/local/bin/cronjob-scripts/
      ```

    * Create shell file inside cronjob directory
      ```cmd
      sudo nano /usr/local/bin/cronjob-scripts/backup_mysql_minutely.sh
      ```

    * Create shell file inside cronjob directory
      ```cmd
      #!/bin/bash

      # MySQL credentials
      USER="<username>"
      PASSWORD="<password>"
      DATABASE="<db_name>"
      
      # Backup directory (ensure this exists or create it)
      BACKUP_DIR="/var/backups/mysql/minutely"
      if [ ! -d "$BACKUP_DIR" ]; then
          echo "Backup directory does not exist. Creating it..."
          mkdir -p "$BACKUP_DIR"
      fi
      
      # S3 Bucket details
      S3_BUCKET="<bucket_name>"
      S3_PATH="<path_inside_bucket>"
      
      # Retention policy (number of days to keep backups)
      RETENTION_DAYS=7
      
      # Get current date for backup filename
      DATE=$(date +%Y%m%d_%H%M%S)
      
      # Create backup file
      BACKUP_FILE="$BACKUP_DIR/$DATABASE-$DATE.sql.gz"
      
      # Perform the backup using mysqldump
      mysqldump -u$USER -p$PASSWORD $DATABASE | gzip > $BACKUP_FILE
      
      # Check if the backup was successful
      if [ $? -eq 0 ]; then
          echo "Backup of $DATABASE completed successfully: $BACKUP_FILE"
      else
          echo "Backup of $DATABASE failed."
          exit 1  # Exit if backup fails
      fi
      
      # Upload to S3
      aws s3 cp "$BACKUP_FILE" s3://$S3_BUCKET/$S3_PATH/$(basename $BACKUP_FILE)
      
      # Check if the S3 upload was successful
      if [ $? -eq 0 ]; then
          echo "Backup uploaded to S3 successfully: s3://$S3_BUCKET/$S3_PATH/$(basename $BACKUP_FILE)"
      else
          echo "Failed to upload backup to S3."
          exit 1  # Exit if S3 upload fails
      fi
      
      # Cleanup: Remove backups older than RETENTION_DAYS
      find $BACKUP_DIR -type f -name "$DATABASE-*.sql.gz" -mtime +$RETENTION_DAYS -exec rm -f {} \;
      
      # Check if any old backups were deleted
      if [ $? -eq 0 ]; then
          echo "Old backups older than $RETENTION_DAYS days have been deleted."
      else
          echo "No backups were deleted (check if any are older than $RETENTION_DAYS days)."
      fi
      ```

    * Set .sh file owner and mode
      ```cmd
      sudo chown <username>:<username> <path_to_cronjob_sh_file>
      sudo chmod 700 <path_to_cronjob_sh_file>
      ```

    * Open **Cronjob Editon**
      ```cmd
      crontab -e
      ```

    * Add this line to the editon then save 
      ```cmd
      0 * * * * /usr/local/bin/cronjob-scripts/backup_mysql_minutely.sh
      ```
      

13. **Project permission**

      ```cmd
      sudo chmod 775 /var/www/<project-name>
      ```
