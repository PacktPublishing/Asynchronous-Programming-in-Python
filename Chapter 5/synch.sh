#!/bin/bash
gunicorn -w 1 --name ch5 --threads 1 --timeout 1 --backlog 0 --bind 127.0.0.1:8080 app_flask:app
#curl -X POST http://localhost:8080/classify?id=112345&image=@/img/1.jpg -H 'Content-Type: multipart/form-data'