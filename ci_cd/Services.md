### `root` user
https://www.digitalocean.com/community/tutorials/how-to-install-jenkins-on-ubuntu-22-04
https://www.digitalocean.com/community/tutorials/how-to-configure-jenkins-with-ssl-using-an-nginx-reverse-proxy-on-ubuntu-22-04
#### **Install Docker**
  ```
  sudo apt update;
  sudo apt install apt-transport-https ca-certificates curl software-properties-common;
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null;
  sudo apt update;
  apt-cache policy docker-ce;
  sudo apt install docker-ce;
  sudo systemctl status docker;
  ```

#### **Install Jenkins**
  ```
  sudo apt install default-jdk;
  wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key |sudo gpg --dearmor -o /usr/share/keyrings/jenkins.gpg;
  sudo sh -c 'echo deb [signed-by=/usr/share/keyrings/jenkins.gpg] http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list';
  sudo apt update;
  sudo apt install jenkins;
  sudo systemctl start jenkins.service;
  sudo ufw allow 8080;
  ```

  ```
  forward port: from local machine: 127.0.0.1:8080 to remote server: 127.0.0.1:8080
  open in web browser on local machine: http://127.0.0.1:8080
  Unlock Jenkins
  ```
  
  ```
  sudo cat /var/lib/jenkins/secrets/initialAdminPassword
  copy&paste password
  ...
  Instance Configuration: http://VDS_IP:8080/
  ```
  
  ```
  select: "Install suggested plugins"
  ```
#### **Install Nginx**  

  ```
  apt update;
  apt install nginx;
  ufw allow 'Nginx HTTP';
  ```
  
  ```
  forward port: from local machine: 127.0.0.1:5000 to remote server: 127.0.0.1:80
  ```
  
  - **Setting Up Server Blocks**
  
    ```
    mkdir -p /var/www/SUBDOMAIN/html;
    chown -R $USER:$USER /var/www/SUBDOMAIN/html;
    chmod -R 755 /var/www/SUBDOMAIN;
    ```
    
    - *index.html*
      ```
      nano /var/www/SUBDOMAIN/html/index.html
      ```
      ```
      <html>
          <head>
              <title>Welcome to SUBDOMAIN!</title>
          </head>
          <body>
              <h1>Success!  The SUBDOMAIN server block is working!</h1>
          </body>
      </html>
      ```
      
    - *SUBDOMAIN*

      ```
      nano /etc/nginx/sites-available/SUBDOMAIN
      ```
      ```
      server {
              listen 80;
              listen [::]:80;

              root /var/www/SUBDOMAIN/html;
              index index.html index.htm index.nginx-debian.html;

              server_name SUBDOMAIN www.SUBDOMAIN;

              location / {
                      try_files $uri $uri/ =404;
              }
      }
      ```
    ```
    ln -s /etc/nginx/sites-available/SUBDOMAIN /etc/nginx/sites-enabled/;
    ```
    ```
    sudo nano /etc/nginx/nginx.conf;
    Uncomment: server_names_hash_bucket_size 64;
    Uncomment: server_tokens off;
    ```
    ```
    nginx -t;
    systemctl restart nginx;
    ```
    ```
    open in web browser on local machine: http://SUBDOMAIN
    ```
    
  - **Secure Nginx with Let's Encrypt**
    ```
    sudo snap install core;
    sudo snap refresh core;
    sudo apt remove certbot;
    sudo snap install --classic certbot;
    ```
    ```
    sudo ufw allow 'Nginx Full';
    sudo ufw delete allow 'Nginx HTTP';
    ```
    ```
    sudo certbot --nginx -d SUBDOMAIN -d www.SUBDOMAIN;
    sudo systemctl status snap.certbot.renew.service;
    sudo certbot renew --dry-run;
    ```