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
   
2. Setup domain name (nginx)
   ```cmd
   sudo nano /etc/nginx/sites-available/default
   ```
   * Update the file with this:
   ```cmd
   server {
     listen 80;
     server_name <domain_name> www.<domain_name>;
   }
   ```

3. Flask app
   * Install python, pip & virtual environment
   ```cmd
   sudo apt install python3-pip python3-venv
   ```
   * Install git
   ```cmd
   sudo apt install git
   ```
   * Clone app from github
   ```cmd
   cd /var/www
   git clone <repository-url>
   ```
   * Setup flask app
   ```cmd
   cd <project-path>
   python3 -m venv .venv
   . .venv/bin/activate
   pip3 install -r requirements.txt
   ```
   * Install gunicorn (Production)
   ```cmd
   sudo apt install gunicorn
   ```
   ```cmd
   sudo gunicorn --bind 0.0.0.0:80 app:app
   ```
