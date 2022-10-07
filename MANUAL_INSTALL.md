### `${PROJECT_USER}`

**Upload source code to `/var/${PROJECT_USER}/${PROJECT_NAME}/`**

```
sudo apt --assume-yes install postgresql postgresql-contrib;
sudo apt --assume-yes install redis;
sudo mkdir -p var/${PROJECT_USER}/${PROJECT_NAME};
sudo chown -R ${PROJECT_USER} /var/${PROJECT_USER}/
pip install -r var/${PROJECT_USER}/${PROJECT_NAME}/requirements.txt;
```

```
cp /var/${PROJECT_USER}/${PROJECT_NAME}/${PROJECT_NAME}.service /etc/systemd/system/
cp -a /var/${PROJECT_USER}/${PROJECT_NAME}/data/database/schema.sql /tmp;  
sudo -i -u postgres;  
createdb ${DB_NAME}; 
psql -d ${DB_NAME} -c "CREATE schema schema;";
psql -d ${DB_NAME} -c "SET schema 'schema';";
psql -d ${DB_NAME} -c "ALTER USER ${POSTGRESS_USER} PASSWORD ${POSTGRESS_PASS};";
psql -d ${DB_NAME} -a -q -f /tmp/schema.sql;
exit && clear;
```

```
systemctl daemon-reload;
systemctl enable ${PROJECT_NAME}.service;
systemctl start ${PROJECT_NAME}.service;
systemctl status ${PROJECT_NAME}.service;
```