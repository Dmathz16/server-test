# Server Test

Used for testing server only


## After running new instance in AWS EC2

```cmd
 sudo apt update
 ```

1. Web Server (nginx)
  ```cmd
  sudo apt install nginx
  ```
  ```cmd
  sudo systemctl start nginx
  sudo systemctl enable nginx
  ```

2. Flask app (nginx)
   * Install python & pip
   ```cmd
   sudo apt install python3-pip
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
