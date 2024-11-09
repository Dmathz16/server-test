# Server Test

Used for testing server only


## After running new instance in AWS EC2

```cmd
 sudo apt update
 ```

1. Change root password then use root account
   ```cmd
   sudo passwd root
   ```
   ```cmd
   su - root
   ```

2. Web Server (nginx)
   ```cmd
   sudo apt install nginx
   ```
   ```cmd
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```
   you can now open the site in browser using your Ip Address

3. Flask app
   * Install python, pip, virtual environment & git
   ```cmd
   sudo apt install python3-pip python3-venv git
   ```
   * Clone app from github
   ```cmd
   cd /var/www
   git clone <repository-url>
   ```
   * Activate virtual environment and setup flask app
   ```cmd
   cd <project-path>
   python3 -m venv .venv
   . .venv/bin/activate
   pip3 install -r requirements.txt
   ```
   * Install gunicorn then bind app
   ```cmd
   pip3 install gunicorn
   ```
   ```cmd
   gunicorn --bind 127.0.0.1:5000 application:app
   ```
4. Setup nginx configuration
   Stop gunicorn then:
   ```cmd
   sudo nano /etc/nginx/sites-available/default
   ```
   * Update the file with this then save:
   ```cmd
   server {
       listen 80;
       server_name your_domain.com;  # Replace with your domain or server IP
   
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
   * Check for syntax error
   ``` cmd
   sudo nginx -t
   ```
   * Restart nginx 
   ``` cmd
   sudo systemctl restart nginx
   ```
   * Change dir to project, activate environment then run gunicorn
   ``` cmd
   gunicorn --bind 127.0.0.1:5000 application:app
   ```
   You can now access the app using domain/ip address

5. Run in production
   Stop gunicorn then create system service:
   ``` cmd
   sudo nano /etc/systemd/system/<service-name>.service
   ```
   * Add configuration then save:
   ``` cmd
   [Unit]
   Description=My app description
   After=network.target
   
   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/dmathz-app
   Environment="PATH=/var/www/dmathz-app/venv/bin"
   ExecStart=/var/www/dmathz-app/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 application:app
   
   [Install]
   WantedBy=multi-user.target
   ```
   * Start and enable the service
   ``` cmd
   sudo systemctl daemon-reload
   sudo systemctl start <service-name>
   sudo systemctl enable <service-name>
   ```
   You can now access the app using domain/ip address without manually running gunicorn
6. Enable firewall (production)
   ``` cmd
   sudo ufw enable
   sudo ufw allow 80/tcp       # Allow HTTP
   sudo ufw allow 443/tcp      # Allow HTTPS
   sudo ufw allow 22/tcp       # Allow SSH
   ```
   Check status
   ``` cmd
   sudo ufw status
   ```
