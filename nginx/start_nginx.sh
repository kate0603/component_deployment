#!/bin/bash

if [ "$ENVIRONMENT" = "dev" ]; then
    cp /etc/nginx/conf.d/default_dev.conf /etc/nginx/conf.d/default.conf
elif [ "$ENVIRONMENT" = "pro" ]; then
    cp /etc/nginx/conf.d/default_pro.conf /etc/nginx/conf.d/default.conf
fi

# Start cron service
cron

# Start Nginx
nginx -g 'daemon off;'