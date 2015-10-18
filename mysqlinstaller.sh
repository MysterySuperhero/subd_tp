#! /usr/bin/env bash
# B4#skM67R2sX
# Variables
APPENV=local
DBHOST=localhost
DBNAME=db
DBUSER=root
DBPASSWD=root

echo -e "\n--- Installing now... ---\n"

echo -e "\n--- Updating packages list ---\n"
apt-get update

echo -e "\n--- Installing base packages ---\n"
apt-get install vim curl git python-pip> /dev/null 2>&1

echo -e "\n--- Installing python packages ---\n"
pip install flask> /dev/null 2>&1

echo -e "\n--- Install MySQL specific packages and settings ---\n"
echo "mysql-server mysql-server/root_password password $DBPASSWD" | debconf-set-selections
echo "mysql-server mysql-server/root_password_again password $DBPASSWD" | debconf-set-selections
apt-get update
apt-get -y install mysql-server> /dev/null 2>&1

echo -e "\n--- Done! ---\n"