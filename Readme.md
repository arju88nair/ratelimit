# The Throttler

## Requirments

```
Python
Django
Redis
```


## Task at hand

    Design a layer to protect a Django powered website from DOS attacks. If a client issues >= 100 requests in a 60s window, return HTTP status = 403 to the client, else the request should be allowed to proceed.

Found out that it can be achieved on 3 levels :


### Local scope

 By using a package called [`ratelimit`](https://django-ratelimit.readthedocs.io/en/stable/usage.html#) which will help us to achieve more or less in a function scoped limiting calls

 > Shown in the views.py inside the app

 ###  Wrapper or global scopped

 Decided to go as a middleware class which uses Redis to store the hash of the IP of the user and increments everytime if it's set and returns 403 if it reaches the limit

 > Shown in the `Throttler` file under `middleware` folder.

 ### [True global level](https://www.nginx.com/blog/deploying-nginx-plus-as-an-api-gateway-part-2-protecting-backend-services/)

 Freedom of going on server level.

 If the Django application is configured in `Nginx` with `uwsgi`, for an example server block as below (taken from my personal server block of Django application),

```
limit_req_zone $binary_remote_addr zone=client_ip_10rs:1m rate=10r/s;  // 10 requests per second
limit_req_status 430; // Customn 403 error
server {
    server_name blah.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/nair/blah;
    }

    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:/run/uwsgi/blah.sock;
    }

}
```
