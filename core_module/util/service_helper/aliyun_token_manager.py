#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import requests
import time
import uuid
from urllib import parse
import os
import json
import time

CACHE_DIR = "cache"
CACHE_FILE = os.path.join(CACHE_DIR, "aliyun_token.json")

from core_module.util.config_librarian import ConfigLibrarian

#Do not import this class
class AccessToken:
    @staticmethod
    def _encode_text(text):
        encoded_text = parse.quote_plus(text)
        return encoded_text.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')
    @staticmethod
    def _encode_dict(dic):
        keys = dic.keys()
        dic_sorted = [(key, dic[key]) for key in sorted(keys)]
        encoded_text = parse.urlencode(dic_sorted)
        return encoded_text.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')
    
    @staticmethod
    def create_token(access_key_id, access_key_secret):
        # Prepare request parameters
        parameters = {
            'AccessKeyId': access_key_id,
            'Action': 'CreateToken',
            'Format': 'JSON',
            'RegionId': 'cn-shanghai',
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureNonce': str(uuid.uuid1()),  # Unique random value to avoid replay attacks
            'SignatureVersion': '1.0',
            'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),  # UTC time in ISO 8601 format
            'Version': '2019-02-28'
        }

        # Generate normalized query string
        query_string = AccessToken._encode_dict(parameters)
        print('Normalized query string: %s' % query_string)

        # Generate string to sign
        string_to_sign = 'GET' + '&' + AccessToken._encode_text('/') + '&' + AccessToken._encode_text(query_string)
        print('String to sign: %s' % string_to_sign)

        # Calculate HMAC-SHA1 signature
        secreted_string = hmac.new(
            bytes(access_key_secret + '&', encoding='utf-8'),
            bytes(string_to_sign, encoding='utf-8'),
            hashlib.sha1
        ).digest()

        # Encode signature with Base64
        signature = base64.b64encode(secreted_string)
        print('Signature (Base64): %s' % signature)

        # URL encode the signature
        signature = AccessToken._encode_text(signature)
        print('URL encoded signature: %s' % signature)

        # Assemble full URL
        full_url = 'http://nls-meta.cn-shanghai.aliyuncs.com/?Signature=%s&%s' % (signature, query_string)
        print('Request URL: %s' % full_url)

        # Send HTTP GET request
        response = requests.get(full_url)

        # Process response
        if response.ok:
            root_obj = response.json()
            key = 'Token'
            if key in root_obj:
                token = root_obj[key]['Id']
                expire_time = root_obj[key]['ExpireTime']
                return token, expire_time

        # Print error response if request failed
        print(response.text)
        return None, None
    

_cached_token = {}
_loaded = False

def get_aliyun_token():
    global _cached_token, _loaded

    cache_dir = ConfigLibrarian.get_cache_dir("token")
    cache_file = os.path.join(cache_dir, "aliyun_token.json")

    print("[AliyunTokenManager] Trying to load aliyun token...")

    # First time loading from file if not already loaded
    if not _loaded:
        if os.path.exists(cache_file):
            print(f"[AliyunTokenManager] Found cache file: {cache_file}")
            with open(cache_file, "r") as f:
                _cached_token = json.load(f)
            print(f"[AliyunTokenManager] Loaded cached token from file.")
        else:
            print(f"[AliyunTokenManager] No cache file found at {cache_file}.")
        _loaded = True

    token = _cached_token.get("token")
    expire_time = _cached_token.get("expire_time", 0)

    # If cached token exists and is not expired, use it
    if token and time.time() < expire_time:
        print("[AliyunTokenManager] Using cached token (runtime memory, valid).")
        return token
    else:
        if token:
            print("[AliyunTokenManager] Cached token expired or invalid, generating new token.")
        else:
            print("[AliyunTokenManager] No valid token found, generating new token.")

    # Generate new token
    service_config = ConfigLibrarian.get_service_config("aliyun")
    access_key_id = service_config["access_id"]
    access_key_secret = service_config["access_secret"]
    token, expire_time = AccessToken.create_token(access_key_id, access_key_secret)

    print(f"[AliyunTokenManager] New token: {token}, expires at (epoch): {expire_time}")
    if expire_time:
        print('[AliyunTokenManager] Token valid until (Beijing Time): %s' %
              time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expire_time)))

    # Save to memory and file
    _cached_token = {"token": token, "expire_time": expire_time}
    os.makedirs(cache_dir, exist_ok=True)
    with open(cache_file, "w") as f:
        json.dump(_cached_token, f)
    print(f"[AliyunTokenManager] Token cached to file: {cache_file}")

    return token