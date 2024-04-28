#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "You should provide exactly one argument - path to secrets directory"
    exit 1
fi

openssl rand -base64 512 > $1/access_token_secret
openssl rand -base64 512 > $1/refresh_token_secret
openssl rand -base64 512 > $1/reset_password_token_secret
openssl rand -base64 512 > $1/verification_token_secret
# Be careful rotating this key, this will make all API keys saved in a database inaccessible
echo "Do you want to rotate 'key_encode_secret'? This will make all API keys stored in a database inaccessible"
read -p "(y/n) > " answer
if [[ $answer = [Yy]* ]]; then
    openssl rand -base64 32 > $1/key_encode_secret
fi