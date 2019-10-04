# LuckyCore
A game for CNSS recruit 2019.

## run

```bash
$ docker-compose up -d
```

```bash
$ docker exec -it container_id python manage.py collectstatic
```

- Nginx configure
```nginx
upstream django {
        server unix:/path/to/project/tmp/luckycore.sock;
}



server {
        listen 443 ssl http2;
        listen [::]:443 ssl;
        ssl on;
        http2_push_preload on;
        server_name <host_name>;
        ssl_certificate /path/to/server.crt;
        ssl_certificate_key /path/to/server.key;
        ssl_protocols  TLSv1 TLSv1.1 TLSv1.2;
        charset utf-8;

        location /static {
                alias /path/to/project/luckycore/static_files;
        }

        location / {
                uwsgi_pass django;
                include /etc/nginx/uwsgi_params;
        }
}
```

## create superuser
```bash
$ docker exec -it container_id python manage.py createsuperuser
```

