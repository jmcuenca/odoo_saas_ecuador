FROM python:3.11-slim-bullseye

# 1. Install System Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    postgresql-client \
    git \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# 2. Install RTLCSS (Required for Odoo 18)
RUN npm install -g rtlcss

# 3. Setup User
RUN useradd -m -d /var/lib/odoo -s /bin/bash odoo

# 4. Install Python Dependencies
COPY odoo-18/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 5. Copy Source Code
WORKDIR /opt/odoo
COPY odoo-18 /opt/odoo
RUN chown -R odoo:odoo /opt/odoo

# 6. Configuration
ENV ODOO_RC /etc/odoo/odoo.conf
COPY etc/odoo.conf /etc/odoo/odoo.conf
RUN chown odoo:odoo /etc/odoo/odoo.conf

# 7. Execution
USER odoo
EXPOSE 8069 8071 8072
ENTRYPOINT ["python3", "odoo-bin"]
CMD ["-c", "/etc/odoo/odoo.conf"]
