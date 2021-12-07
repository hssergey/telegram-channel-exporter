#!/bin/sh
cd /var/www/fido.ortoped.org.ru
/usr/bin/find . -mtime +15 -type f -delete
