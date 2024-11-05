# Используем базовый образ Python 3.10 с Debian Bullseye
FROM python:3.10-slim-bullseye

# Устанавливаем необходимые системные пакеты
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libsasl2-dev \
    libldap2-dev \
    libjpeg-dev \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1 \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя 'odoo' и необходимые директории
RUN useradd -m -U -r -d /opt/odoo -s /bin/bash odoo \
    && mkdir -p /var/lib/odoo /etc/odoo /opt/odoo/custom_addons \
    && chown -R odoo:odoo /var/lib/odoo /etc/odoo /opt/odoo/custom_addons

# Переключаемся на пользователя 'odoo'
USER odoo

# Клонируем исходный код Odoo 17 в /opt/odoo/odoo
RUN git clone --depth 1 --branch 17.0 https://github.com/odoo/odoo.git /opt/odoo/odoo

# Устанавливаем Python-зависимости
RUN pip install --user -r /opt/odoo/odoo/requirements.txt

# Устанавливаем переменную окружения PATH для pip пакетов
ENV PATH="/home/odoo/.local/bin:${PATH}"

# Переключаемся обратно на пользователя root для копирования конфигурации
USER root
COPY ./config/odoo.conf /etc/odoo/
RUN chown odoo:odoo /etc/odoo/odoo.conf

# Переключаемся на пользователя 'odoo' и устанавливаем рабочую директорию
USER odoo
WORKDIR /opt/odoo/odoo

# Открываем порт 8069
EXPOSE 8069

# Запускаем Odoo
ENTRYPOINT ["./odoo-bin"]
CMD ["-c", "/etc/odoo/odoo.conf"]

