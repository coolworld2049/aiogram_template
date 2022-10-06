## Initial server setup
### `root` user
```
adduser testbot;
usermod -aG sudo testbot;
sudo ufw allow ssh;
sudo ufw enable;
```

```
sudo apt update && sudo apt upgrade;
apt install python3;
apt install python3-venv;
apt install python3-pip;
apt install postgresql postgresql-contrib;
apt install redis;
```

```
nano /etc/environment
```
- **aiogram_template_env.sh**
    ```
    PROJECT_NAME="aiogram_template"
    PROJECT_USER="testbot"
    DB_NAME="testbot"
    PGUSER="postgres"
    PGPASS="qwerty"
    TZ="Europe/Mocsow"
    ```
### next step: MANUAL_INSTALL or Dockerfile