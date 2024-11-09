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
