#!/usr/bin/env bash
cd /home/adam/zas
docker-compose -f docker-compose.yml -f prod.yml stop
docker run -it --rm -p 443:443 -p 80:80 --name letsencrypt -v "/etc/letsencrypt:/etc/letsencrypt" -v "/var/lib/letsencrypt:/var/lib/letsencrypt" quay.io/letsencrypt/letsencrypt:latest renew
docker-compose -f docker-compose.yml -f prod.yml up -d
