#!/bin/bash

openssl rand -base64 512 > $1/access_token_secret
openssl rand -base64 512 > $1/refresh_token_secret
openssl rand -base64 512 > $1/reset_password_token_secret
openssl rand -base64 512 > $1/verification_token_secret
# Be careful rotating this key, this will make all API keys saved in a database inaccessible
openssl rand -base64 512 > $1/key_encode_key
