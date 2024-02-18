#!/bin/bash

set -e

# Update and install necessary packages
sudo apt-get update
sudo apt-get install -y git gcc make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git

# Install pyenv
curl https://pyenv.run | bash

# Add pyenv to PATH
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc

# Install Python 3.11
pyenv install 3.11
pyenv global 3.11

# Verify Python version
python --version

# Create a directory for your project and change to it
mkdir /home/ubuntu/app
cd /home/ubuntu/app

# Clone your Django project from a Git repository
git clone https://github.com/lambda-py/py_june.git .

# Create a Python virtual environment and activate it
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies from your requirements.txt file
pip install -r requirements.txt gunicorn

# Run Django migrations and collect static files
python manage.py migrate
python manage.py collectstatic --no-input

# Gunicorn systemd service setup
cat > /etc/systemd/system/gunicorn.service << EOF
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/app
ExecStart=/home/ubuntu/app/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/app/app.sock py_june.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Start and enable Gunicorn service
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Nginx configuration to proxy pass to Gunicorn
cat > /etc/nginx/sites-available/app << EOF
server {
    listen 80;
    server_name py-june.dev;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/ubuntu/app/staticfiles/;
    }

    location / {
        proxy_pass http://unix:/home/ubuntu/app/app.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Link Nginx config and restart Nginx
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled
sudo nginx -t && sudo systemctl restart nginx

# Allow traffic on port 80 (HTTP)
sudo ufw allow 'Nginx Full'
