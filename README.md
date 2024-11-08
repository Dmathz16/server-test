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
   * Test run flask app
   ```cmd
   cd <project-path>
   python3 -m venv .venv
   . .venv/bin/activate
   pip3 install -r requirements.txt
   ```
