#!/bin/bash
echo "$SSL_CERTIFICATE" >> cert.pem
echo "$SSL_KEY" >> key.pem
uvicorn main:app --port 8062 --host 0.0.0.0