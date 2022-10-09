## Initial server setup

### `root`

- set: `YOU_USERNAME`

    ```
    adduser YOU_USERNAME;
    usermod -aG sudo $USER;
    sudo ufw allow ssh;
    sudo ufw enable;
    ```
    
- packages

    ```
    apt update && apt upgrade && apt install python3 python3-virtualenv python3-pip redis postgresql postgresql-contrib -y;
    ```

### `$USER`

- `sudo nano .bashrc`

    - set: `PROJECT_NAME` `SOURCE_CODE_LINK` `BOT_TOKEN`
    
        ```
        PROJECT_NAME="YOUR_PROJECT_NAME"
        SOURCE_CODE_LINK="YOUR_SOURCE_CODE_LINK"
        PYTHONUNBUFFERED=1
        BOT_TOKEN="YOUR_BOT_TOKEN"
        ```
    - reboot server: `sudo reboot`
    
- virtualenv

    ```
    sudo rm -rf /var/$USER/$PROJECT_NAME;
    sudo git clone $SOURCE_CODE_LINK /var/$USER/$PROJECT_NAME;
    cd /var/$USER/$PROJECT_NAME;
    sudo chown -R $USER $PWD/;
    virtualenv venv;
    source venv/bin/activate;
    pip install -r $PWD/requirements.txt;
    deactivate
    ```
    
- `sudo nano /etc/systemd/system/$PROJECT_NAME.service`

    ```
    [Unit]
    Description=service
    After=syslog.target
    After=network.target

    [Service]
    Type=simple
    User=$USER
    WorkingDirectory=/var/${USER}/${PROJECT_NAME}
    ExecStart=/bin/sh -c "cd /var/$USER/$PROJECT_NAME/ && source venv/bin/activate && python3 app.py"
    Restart=on-failure
    RestartSec=5s

    [Install]
    WantedBy=multi-user.target
    ```
        
- `cp -a $PWD/data/database/schema.sql /tmp;`

- `sudo -i -u postgres`

    ```
    createdb $PROJECT_NAME; 
    psql -d $PROJECT_NAME -c "CREATE schema schema;";
    psql -d $PROJECT_NAME -c "SET schema 'schema';";
    psql -d $PROJECT_NAME -c "ALTER USER postgres PASSWORD 'postgres';";
    psql -d $PROJECT_NAME -a -q -f /tmp/schema.sql;
    exit;
    ```

- start service

    ```
    sudo systemctl daemon-reload;
    sudo systemctl enable $PROJECT_NAME.service;
    sudo systemctl start $PROJECT_NAME.service;
    sudo systemctl status $PROJECT_NAME.service;
    ```

- update source code

    ```
    cd && sudo rm -rf /var/$USER/$PROJECT_NAME;
    sudo git clone $SOURCE_CODE_LINK /var/$USER/$PROJECT_NAME;
    cd /var/$USER/$PROJECT_NAME && sudo chown -R $USER $PWD/;
    ```
    
    - restart service
    
        ```
        sudo systemctl daemon-reload;
        sudo systemctl restart $PROJECT_NAME.service;
        sudo systemctl status $PROJECT_NAME.service;
        ```
- github-actions
    ```
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    cat github-actions.pub >> ~/.ssh/authorized_keys
    ```
