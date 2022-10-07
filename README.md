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
sudo nano /etc/environment
```

```
PROJECT_NAME="aiogram-template"
```

```
sudo git clone https://github.com/coolworld2049/aiogram-template.git /var/$USER/$PROJECT_NAME
cd /var/$USER/$PROJECT_NAME;
sudo chown -R $USER $PWD/;
pip install -r $PWD/requirements.txt;
sudo nano /etc/systemd/system/$PROJECT_NAME.service;
```

```
[Unit]
Description=$PROJECT_NAME bot
After=syslog.target
After=network.target

[Service]
Type=simple
WorkingDirectory=/var/$USER/$PROJECT_NAME
Environment="PYTHONUNBUFFERED=1"
Environment="BOT_TOKEN=YOUR_BOT_TOKEN"
ExecStart=/usr/bin/python3 /var/$USER/$PROJECT_NAME/app.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

```
sudo -i -u postgres;  
cd /var/$USER/$PROJECT_NAME
cp -a $PWD/data/database/schema.sql /tmp;  
createdb $PWD; 
psql -d $PWD -c "CREATE schema schema;";
psql -d $PWD -c "SET schema 'schema';";
psql -d $PWD -c "ALTER USER postgres PASSWORD 'postgres';";
psql -d $PWD -a -q -f /tmp/schema.sql;
exit;
```

```
sudo systemctl daemon-reload;
sudo systemctl enable aiogram-template.service;
sudo systemctl start aiogram-template.service;
sudo systemctl status aiogram-template.service;
```