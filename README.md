## Initial server setup

```
adduser testbot;
usermod -aG sudo testbot;
sudo ufw allow ssh;
sudo ufw enable;
```

```
apt --assume-yes update;
apt --assume-yes upgrade;
apt --assume-yes install python3;
apt --assume-yes install python3-venv;
apt --assume-yes install python3-pip;
apt --assume-yes install redis;
apt --assume-yes install postgresql postgresql-contrib;
```

### `$USER`

```
sudo rm -rf /var/$USER/$PROJECT_NAME;
sudo git clone https://github.com/coolworld2049/aiogram-template.git /var/$USER/$PROJECT_NAME;
cd /var/$USER/$PROJECT_NAME;
sudo chown -R $USER $PWD/;
pip install -r $PWD/requirements.txt;
sudo nano /etc/systemd/system/$PROJECT_NAME.service;
```

```
[Unit]
Description=service
After=syslog.target
After=network.target

[Service]
Type=simple
User=testbot
WorkingDirectory=/var/$USER/$PROJECT_NAME
Environment="PYTHONUNBUFFERED=1"
Environment="BOT_TOKEN=YOUR_BOT_TOKEN"
Environment="PROJECT_NAME=YOUR_PROJECT_NAME"
ExecStart=/usr/bin/python3 /var/$USER/$PROJECT_NAME/app.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

```
sudo -i -u postgres; 
```
```
cd /var/$USER/$PROJECT_NAME
cp -a $PWD/data/database/schema.sql /tmp;  
createdb $PROJECT_NAME; 
psql -d $PROJECT_NAME -c "CREATE schema schema;";
psql -d $PROJECT_NAME -c "SET schema 'schema';";
psql -d $PROJECT_NAME -c "ALTER USER postgres PASSWORD 'postgres';";
psql -d $PROJECT_NAME -a -q -f /tmp/schema.sql;
exit;
```

```
sudo systemctl daemon-reload;
sudo systemctl enable aiogram-template.service;
sudo systemctl start aiogram-template.service;
sudo systemctl status aiogram-template.service;
```

```
cd
sudo rm -rf /var/$USER/$PROJECT_NAME;
sudo git clone https://github.com/coolworld2049/aiogram-template.git /var/$USER/$PROJECT_NAME;
cd /var/$USER/$PROJECT_NAME;
sudo chown -R $USER $PWD/;
sudo systemctl daemon-reload;
sudo systemctl restart $PROJECT_NAME.service;
sudo systemctl status $PROJECT_NAME.service;
```