## PostgresQL database
![Diagram](https://github.com/coolworld2049/aiogram-template/blob/master/bot.png)
```
CREATE DATABASE test OWNER admin;
CREATE SCHEMA bot;
SET SCHEMA 'bot';

DELETE FROM pg_type WHERE typname = 'base_role';
DELETE FROM pg_type WHERE typname = 'user_state';

CREATE TYPE base_role AS ENUM ('customer', 'contractor', 'admin');
CREATE TYPE user_state AS ENUM (
            'UserStates:creating',
            'UserStates:accepted',
            'UserStates:progress',
            'UserStates:completed',
            'UserStates:terminated'
        );

CREATE TABLE IF NOT EXISTS bot.user (
   user_id BIGINT PRIMARY KEY NOT NULL UNIQUE,
   username TEXT,
   first_name TEXT,
   last_name TEXT,
   state user_state,
   "role" base_role,
   is_admin BOOLEAN,
   last_seen FLOAT
);


CREATE TABLE IF NOT EXISTS bot.order (
   id BIGINT PRIMARY KEY,
   contractor_id  BIGINT REFERENCES bot.user(user_id) NULL,
   customer_id  BIGINT REFERENCES bot.user(user_id) NULL,
   "role" base_role,
   state user_state,
   create_time FLOAT
);

CREATE TABLE IF NOT EXISTS bot.temp (
   user_id BIGINT PRIMARY KEY,
   last_message_id TEXT
);

CREATE OR REPLACE FUNCTION bot.upsert_table_temp(us_id BIGINT, l_msg TEXT) RETURNS VOID AS $$
BEGIN
    UPDATE bot.temp SET last_message_id = $2 WHERE user_id = $1;
    IF NOT FOUND THEN
        INSERT INTO bot.temp values ($1, $2);
    END IF;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION bot.upsert_table_user(us_id BIGINT, is_admin BOOLEAN) RETURNS VOID AS $$
BEGIN
    UPDATE bot.user SET is_admin = $2 WHERE user_id = $1;
    IF NOT FOUND THEN
        INSERT INTO bot.user values ($1, $2);
    END IF;
END;
$$
LANGUAGE plpgsql;
```

## Deploy to VDS [Ubuntu 22.04]

### CI/CD
- **Install Jenkins**
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
- **Install Nginx**  

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
    mkdir -p /var/www/REVERSE_IP/html;
    chown -R $USER:$USER /var/www/REVERSE_IP/html;
    chmod -R 755 /var/www/REVERSE_IP;
    ```
    
    - *index.html*
      ```
      nano /var/www/REVERSE_IP/html/index.html
      ```
      ```
      <html>
          <head>
              <title>Welcome to REVERSE_IP!</title>
          </head>
          <body>
              <h1>Success!  The REVERSE_IP server block is working!</h1>
          </body>
      </html>
      ```
      
    - *REVERSE_IP*

      ```
      nano /etc/nginx/sites-available/REVERSE_IP
      ```
      ```
      server {
              listen 80;
              listen [::]:80;

              root /var/www/REVERSE_IP/html;
              index index.html index.htm index.nginx-debian.html;

              server_name REVERSE_IP www.REVERSE_IP;

              location / {
                      try_files $uri $uri/ =404;
              }
      }
      ```
    ```
    ln -s /etc/nginx/sites-available/REVERSE_IP /etc/nginx/sites-enabled/;
    ```
    ```
    sudo nano /etc/nginx/nginx.conf;
    Uncomment: server_names_hash_bucket_size 64;
    ```
    ```
    nginx -t;
    systemctl restart nginx;
    ```
    ```
    open in web browser on local machine: http://REVERSE_IP
    ```
    
  - **Nginx files and directories**
  
    - **Content**
      `/var/www/html`: The actual web content, which by default only consists of the default Nginx page you saw earlier, is served out of the `/var/www/html`                 directory. This can be changed by altering Nginx configuration files.
    - **Server Configuration**
      - `/etc/nginx`: The Nginx configuration directory. All the Nginx configuration files reside here.
      - `/etc/nginx/nginx.conf`: The main Nginx configuration file. This can be modified to make changes to the Nginx global configuration.
      - `/etc/nginx/sites-available/`: The directory where per-site server blocks can be stored. Nginx will not use the configuration files found in this directory             unless they are linked to the sites-enabled directory. Typically, all server block configuration is done in this directory, and then enabled by linking to the         other directory.
      - `/etc/nginx/sites-enabled/`: The directory where enabled per-site server blocks are stored. Typically, these are created by linking to configuration files             found in the sites-available directory.
      - `/etc/nginx/snippets`: This directory contains configuration fragments that can be included elsewhere in the Nginx configuration. Potentially repeatable                 configuration segments are good candidates for refactoring into snippets.
    - **Server Logs**
      - `/var/log/nginx/access.log`: Every request to your web server is recorded in this log file unless Nginx is configured to do otherwise.
      - `/var/log/nginx/error.log`: Any Nginx errors will be recorded in this log.
  
- **Secure Nginx with Let's Encrypt**
  ```
  sudo snap install core;
  sudo snap refresh core;
  sudo apt remove certbot;
  sudo snap install --classic certbot;
  sudo ln -s /snap/bin/certbot /usr/bin/certbot;
  ```
  - *REVERSE_IP*
    
    ```
    sudo nano /etc/nginx/sites-available/REVERSE_IP;
    server_name REVERSE_IP www.REVERSE_IP;
    ```
  ```
  nginx -t;
  systemctl restart nginx;
  ```
  ```
  sudo ufw allow 'Nginx Full';
  sudo ufw delete allow 'Nginx HTTP';
  ```
  ```
  sudo certbot --nginx -d REVERSE_IP -d www.REVERSE_IP;
  sudo systemctl status snap.certbot.renew.service;
  sudo certbot renew --dry-run;
  ```

### `root` user

```
sudo apt update && sudo apt upgrade;
adduser bot;
usermod -aG sudo bot;
apt install python3;
apt install python3-venv;
apt install python3-pip;
apt install postgresql postgresql-contrib;
apt install redis;
sudo ufw allow ssh;
sudo ufw allow OpenSSH;
sudo ufw enable;
```

### `bot` user

```
sudo mkdir -p home/bot/BOTNAME;
sudo chown -R bot /home/bot/
cd home/bot/BOTNAME;
pip install -r requirements.txt;
python3 -m venv venv;
sudo nano /etc/systemd/system/bot.service;
```

- **bot.service**

  - type `YOUR_PASSWORD`
  - type `YOUR_BOT_TOKEN`
  
    ```
    [Unit]
    Description=bot_service
    After=syslog.target
    After=network.target

    [Service]
    Type=simple
    WorkingDirectory=/home/bot/BOTNAME
    Environment="PYTHONUNBUFFERED=1"
    Environment="BOT_TOKEN=YOUR_BOT_TOKEN"
    Environment="PGADMIN=postgres"
    Environment="PGADMINPASS=YOUR_PASSWORD"
    ExecStart=/usr/bin/python3 /home/bot/BOTNAME/app.py
    Restart=on-failure
    RestartSec=5s

    [Install]
    WantedBy=multi-user.target
    ```

- **postgres database**

  - type `YOUR_PASSWORD`
  
  - **upload source code via SFTP to `/home/bot/BOTNAME/`**
  
  ```
  cp -a /home/bot/BOTNAME/data/supporter_sources/country/country.csv /tmp;
  cp -a /home/bot/BOTNAME/data/supporter_sources/airport/airport.csv /tmp/;
  cp -a /home/bot/BOTNAME/data/database/bot.sql /tmp;  
  systemctl start postgresql.service;
  sudo -i -u postgres;  
  createdb bot; 
  psql -d bot;
  
  CREATE schema bot;
  SET schema 'bot';
  ALTER USER postgres PASSWORD 'YOUR_PASSWORD';
  ```
  ```
  \i /tmp/bot.sql
  ```
  ```
  COPY bot.country FROM '/tmp/country.csv' DELIMITER ',' CSV HEADER;
  COPY bot.airport FROM '/tmp/airport.csv' DELIMITER ',' CSV HEADER;
  ```
  ```
  \q
  ```
  ```
  exit && clear;
  ```

- **systemctl commands**
  ```
  systemctl daemon-reload;
  systemctl enable bot.service;
  systemctl start bot.service;
  systemctl status bot.service;
  ```
