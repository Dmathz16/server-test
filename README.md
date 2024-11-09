# Server Test

Used for testing server only


## After running new instance in AWS EC2

```cmd
sudo apt update
```

1. **Create web server (nginx)**
   ```cmd
   sudo apt install nginx
   ```
   ```cmd
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```

2. **Manage users**
   
   **Change root password**

   ```cmd
   sudo passwd root
   ```

   **Create new user**

   * Create user group named "server_admin" 
   ```cmd
   sudo groupadd server_admin
   ```
   
   * Create user named "rogin" then assign to "server_admin" 
   ```cmd
   sudo useradd -m -g server_admin -s /bin/bash rogin
   ```
   
   * Create user "rogin" password 
   ```cmd
   sudo passwd rogin
   ```
   
   * Set "server_admin" permissions for web server files.
   ```cmd
   sudo chown -R :server_admin /var/www
   sudo chmod -R 775 /var/www
   ```
   
   * Add "rogin" to the "server_admin" group, if not done yet.
   ``` cmd
   sudo usermod -aG server_admin rogin
   ```
   
   * Set Permissions for the Web Server to Run as "www-data"
      * Modify directive
      ``` cmd
      sudo nano /etc/nginx/nginx.conf
      ```
      * Update to
      ``` cmd
      user www-data server_admin;
      ```
   
   * Verify Group Membership
   ``` cmd
   groups rogin
   ```
   
   * Add "rogin" to sudo group
   ``` cmd
   sudo usermod -aG sudo rogin
   ```

   **Remove "ubuntu" user**
   
   * Check running processes
   ``` cmd
   ps -u ubuntu
   ```

   * Terminate "ubuntu" Active Session
   ``` cmd
   sudo kill <PID>
   ```

   * Remove the user
   ``` cmd
   sudo userdel -r ubuntu
   ```

   **Restart Web Server**
   ``` cmd
   sudo systemctl restart nginx
   ```
  
   **Login as "rogin" directly**
   ``` cmd
   su - rogin
   ```
