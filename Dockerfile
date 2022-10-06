FROM python:3.10 as production
LABEL maintainer="Nikita Ivanov <coolworld2049@gmail.com>" description="aiogram_bot_template"

WORKDIR /var/bot/aiogram_bot_template

USER bot

RUN sudo mkdir -p home/bot/aiogram_bot_template && \
    sudo chown -R bot /home/bot/ && \
    cd home/bot/aiogram_bot_template && \
    pip install -r requirements.txt && \
    python3 -m venv venv && cd

RUN cp /var/bot/aiogram_bot_template/bot_template.service /etc/systemd/system/

RUN cp -a /var/bot/aiogram_bot_template/data/database/bot.sql /tmp


RUN systemctl start postgresql.service \

USER postgres

RUN sudo -i -u postgres && \
    createdb bot && \
    psql -d bot -c "CREATE schema bot;" && \
    psql -d bot -c "SET schema 'bot';" && \
    psql -d bot -c "ALTER USER postgres PASSWORD 'qwerty';" && \
    psql -U postgres -d bot -a -q -f /tmp/bot.sql && \
    psql -d bot -c "COPY bot.country FROM '/tmp/country.csv' DELIMITER ',' CSV HEADER;" && \
    psql -d bot -c "COPY bot.airport FROM '/tmp/airport.csv' DELIMITER ',' CSV HEADER;" && \
    exit && clear

USER bot

CMD systemctl daemon-reload && \
    systemctl enable bot.service && \
    systemctl start bot.service && \
    systemctl status bot.service