#!/usr/bin/env bash
# A script that sets up your web servers for deployment

# Install nginx
sudo apt-get -y update
sudo apt-get -y install nginx

# Create the folder if they don't exists
sudo mkdir -p /data/ /data/web_static/ /data/web_static/releases/ /data/web_static/shared/ /data/web_static/releases/test/

# A simple HTML file
echo "Hey" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Delete the current directory if exists and create a symbolic link
sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Change the owner of /data to ubuntu
sudo chown -R ubuntu:ubuntu /data/

# update the Nginx configuration to serve content
update="\\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"
sudo sed -i "38i $update" /etc/nginx/sites-available/default

# Restart Nginx service
sudo service nginx restart
