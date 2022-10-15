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
    apt update && apt upgrade && apt -y install python3 python3-virtualenv python3-pip redis postgresql postgresql-contrib;
    ```

### `$USER`

- `cd && sudo nano .bashrc`

    - set: `PROJECT_NAME` `SOURCE_CODE_LINK` `BOT_TOKEN`
    
        ```
        PROJECT_NAME="YOUR_PROJECT_NAME"
        SOURCE_CODE_LINK="YOUR_SOURCE_CODE_LINK"
        ```
    - reboot server: `sudo reboot`
    
- virtualenv

    ```
    sudo rm -rf /var/$USER/$PROJECT_NAME;
    sudo git clone $SOURCE_CODE_LINK /var/$USER/$PROJECT_NAME;
    cd /var/$USER/$PROJECT_NAME;
    sudo chown -R $USER $PWD/;
    python3 -m virtualenv venv;
    source venv/bin/activate;
    pip install -r $PWD/requirements.txt;
    deactivate
    ```
    
- `sudo nano /etc/systemd/system/$PROJECT_NAME.service`

  - set: `USER` `PROJECT_NAME` `BOT_TOKEN`
  
      ```
      [Unit]
      Description=service
      After=network.target

      [Service]
      Type=simple
      WorkingDirectory=/var/$USER/$PROJECT_NAME
      ExecStart=bash -c "cd /var/$USER/$PROJECT_NAME/ && source venv/bin/activate && python3 app.py"
      Restart=on-failure
      RestartSec=30s

      [Install]
      WantedBy=multi-user.target
      ```
    
- postgres

    ```
    sudo -u postgres psql -d postgres -c "CREATE DATABASE $PROJECT_NAME;";
    sudo -u postgres psql -d $PROJECT_NAME -c "CREATE SCHEMA schema;" -c "SET schema 'schema';"
    sudo -u postgres psql -d $PROJECT_NAME -c "ALTER USER postgres PASSWORD 'postgres';"
    sudo -u postgres psql -d $PROJECT_NAME -f /var/$USER/$PROJECT_NAME/schema.sql
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
    sudo rm -rf /var/$USER/$PROJECT_NAME;
    sudo git clone $SOURCE_CODE_LINK /var/$USER/$PROJECT_NAME;
    cd /var/$USER/$PROJECT_NAME;
    sudo chown -R $USER $PWD/;
    python3 -m virtualenv venv;
    source venv/bin/activate;
    pip install -r $PWD/requirements.txt;
    deactivate
    ```
    
    - restart service
    
        ```
        sudo systemctl daemon-reload;
        sudo systemctl restart $PROJECT_NAME.service;
        sudo systemctl status $PROJECT_NAME.service;
        ```