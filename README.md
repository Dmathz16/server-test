# Server Test

Used for testing server only


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

2. **Set server account**
   
   2.1. Change root password
      ```cmd
      sudo passwd root
      ```
   
   2.2. Add new user
      ```cmd
      sudo -i
      ```
      ```cmd
      adduser <new-user>
      ```
      Add user to sudo group
      ```cmd
      usermod -aG sudo <new-user>
      ```
      Add user to www-data group and set permission
      ```cmd
      usermod -aG www-data <new-user>
      sudo chmod -R 775 /var/www
      sudo chown -R <new-user>:www-data /var/www
      ```
      Open sshd_config file
      ```cmd
      nano /etc/ssh/sshd_config
      ```
      Uncomment code like this then save
      ```cmd
      PasswordAuthentication yes
      ```
      Restart ssh service
      ```cmd
      sudo systemctl restart ssh.service
      ```
      Set new user ssh access 
      ```cmd
      sudo mkdir -p /home/<new-user>/.ssh
      sudo chmod 700 /home/<new-user>/.ssh
      sudo cp /home/<old-user>/.ssh/authorized_keys /home/<new-user>/.ssh/authorized_keys
      ```
      ```cmd
      sudo chmod 600 /home/<new-user>/.ssh/authorized_keys
      sudo chown -R <new-user>:<new-user> /home/<new-user>/.ssh
      ```
      
   2.3. Remove default user named **ubuntu**
      Show processes running under ubuntu
      ```cmd
      ps -u ubuntu
      ```
      Kill process one by one with PID(Process ID) using this
      ```cmd
      sudo kill <PID>
      ```
      Remove **ubuntu** user if all processes has been killed
      ```cmd
      sudo userdel -r ubuntu
      ```
      Exit root session
      ```cmd
      exit
      ```
   
4. **Set MySQL server** (If needed)
   Install and setup server
   ```cmd
   sudo apt-get install mysql-server
   sudo mysql_secure_installation
   sudo systemctl status mysql
   ```
   Connect to MySQL server
   ```cmd
   sudo mysql -u root -p
   ```
   Create database
   ```cmd
   CREATE DATABASE <db_name>;
   SHOW DATABASES;
   EXIT;
   ```
   Import existing sql
   ```cmd
   sudo mysql -u root -p <db_name> < <path_to_sql_file>
   ```
   Check if data are imported
   ```cmd
   sudo mysql -u root -p
   SHOW DATABASES;
   USE <db_name>;
   SELECT * FROM <table_name>;
   EXIT;
   ```

5. **Set flask app**
   4.1. Install app and other requirements
   4.2. Run with gunicorn + wsgi 
   
6. **Set nginx config**
   5.1. Domain name
