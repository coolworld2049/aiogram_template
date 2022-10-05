# Deploy to VDS [Ubuntu 22.04]

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
