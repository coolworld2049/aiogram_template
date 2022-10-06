### `${PROJECT_USER}` user
```
sudo mkdir -p var/${PROJECT_USER}/${PROJECT_NAME};
sudo chown -R ${PROJECT_USER} /var/${PROJECT_USER}/
cd var/${PROJECT_USER}/${PROJECT_NAME};
pip install -r requirements.txt;
python3 -m venv venv;
cp /var/${PROJECT_USER}/${PROJECT_NAME}/${PROJECT_NAME}.service /etc/systemd/system/
```
- **postgres database**
  - **upload source code to `/var/${PROJECT_USER}/${PROJECT_NAME}/`**
  ```
  cp -a /var/${PROJECT_USER}/${PROJECT_NAME}/data/database/schema.sql /tmp;  
  systemctl start postgresql.service;
  sudo -i -u postgres;  
  createdb ${DB_NAME}; 
  psql -d ${DB_NAME} -c "CREATE schema schema;";
  psql -d ${DB_NAME} -c "SET schema 'schema';";
  psql -d ${DB_NAME} -c "ALTER USER postgres PASSWORD ${POSTGRESS_PASS};";
  psql -d ${DB_NAME} -a -q -f /tmp/schema.sql;
  exit && clear;
  ```

- **systemctl commands**
  ```
  systemctl daemon-reload;
  systemctl enable ${PROJECT_NAME}.service;
  systemctl start ${PROJECT_NAME}.service;
  systemctl status ${PROJECT_NAME}.service;
  ```