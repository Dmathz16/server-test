# Server Test

Used for testing server only


## After running new instance in AWS EC2

**Connect to server using SSH in terminal**
```cmd
ssh -i <path_to_pem_file> ubuntu@<ipaddress>
```

**Update ubuntu software**
```cmd
sudo apt update
```

1 **Install and enable web server (nginx)**
   ```cmd
   sudo apt install nginx -y
   ```
   ```cmd
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```

2 **Set server account**
   2.1 Change root password
   2.2 Add new user
   2.3 Remove default user
   
3 **Set MySQL server**

4 **Set flask app**
   4.1 Install app and other requirements
   4.2 Run with gunicorn + wsgi 
   
5 **Set nginx config**
   5.1 Domain name
