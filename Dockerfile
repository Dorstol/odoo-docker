FROM odoo:16.0

# Switch to root user to install necessary packages
USER root

# Install wget and add the PostgreSQL repository for potential compatibility
RUN apt-get update && apt-get install -y wget gnupg && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ bullseye-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    mkdir -p /usr/share/keyrings && \
    wget -qO /usr/share/keyrings/pgdg-archive-keyring.gpg https://www.postgresql.org/media/keys/ACCC4CF8.asc

# Install odoo-helper-scripts and pre-requirements without downgrading libpq5
RUN apt-get update && apt-get install -y libpq-dev && \
    wget -O - https://gitlab.com/katyukha/odoo-helper-scripts/raw/master/install-system.bash | bash -s && \
    odoo-helper install pre-requirements && \
    rm -rf /var/lib/apt/lists/*

# Switch back to the odoo user
USER odoo

