# https://testdriven.io/blog/fastapi-jwt-auth/
# https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
import binascii
import hashlib
import os
import time
from datetime import datetime
from typing import Dict, Optional

import jwt
import numpy as np
from fastapi import HTTPException
from loguru import logger

from backend.db import RedisHandler
from config import conf
from models.user import User


class AuthHandler(object):
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            logger.info(f"Instantiating AuthHandler!")
            cls.__singleton = super(AuthHandler, cls).__new__(cls)

            cls.__auth = RedisHandler().get_auth_client()

            cls.__admin_pwd = conf.backend.auth.admin_pwd
            cls.__admin_id = conf.backend.auth.admin_id
            cls.__jwt_algo = conf.backend.auth.jwt_algo
            cls.__jwt_ttl = conf.backend.auth.jwt_ttl

            if conf.backend.auth.jwt_secret == '':
                logger.warning('JWT Secret not provided! Generating 32 bit secret')
                cls.__jwt_secret = binascii.hexlify(os.urandom(32))
            else:
                cls.__jwt_secret = conf.backend.auth.jwt_secret

        return cls.__singleton

    def register_admin(self):
        # we wait a random amount of time here to support multi-processing (gunicorn spawns multiple processes) so
        # only the instance that reads the init_flag first will init Redis! Otherwise it gets initialized multiple
        # times
        time.sleep(np.random.uniform(low=0.3, high=1.0))
        try:
            u = User(id=self.__admin_id, password=self.__admin_pwd)
            self.register(u)
            self.__add_admin_user(u)
        except Exception as e:
            pass

    def __get_jwt(self, user: User) -> Dict[str, str]:
        # try to load from cache
        token = self.__get_cached_token(user)
        if token is None:
            payload = {
                'user_id': user.id,
                'ttl': time.time() + self.__jwt_ttl
            }
            logger.debug(f"Generated JWT for {user.id} that expires at {datetime.fromtimestamp(payload['ttl'])}!")
            token = jwt.encode(payload, self.__jwt_secret, algorithm=self.__jwt_algo)
            self.__cache_token(user, token)
        return {'jwt': token}

    def decode_jwt(self, token: str) -> Optional[Dict]:
        try:
            decoded = jwt.decode(token, self.__jwt_secret, algorithms=self.__jwt_algo)
            return decoded
        except Exception as e:
            logger.error(f"Cannot decode JWT! Exception: {e}")
            return None

    def __add_admin_user(self, user: User):
        logger.debug(f"Add User {user.id} to administrators!")
        self.__auth.rpush('admin_users'.encode('utf-8'), user.id.encode('utf-8'))

    def is_admin(self, user_id: str) -> bool:
        admin_users = self.__auth.lrange('admin_users'.encode('utf-8'), 0, -1)
        return user_id.encode('utf-8') in admin_users

    def __store_salt(self, user: User) -> bytes:
        logger.debug(f"Generating 32 Bit PBKDF2 Salt for User {user.id}")
        salt = os.urandom(32)
        self.__auth.set(str(user.id + '_salt').encode('utf-8'), salt, nx=True)
        return salt

    def __get_salt(self, user: User) -> Optional[bytes]:
        salt = self.__auth.get(str(user.id + '_salt').encode('utf-8'))
        if salt is None:
            logger.warning(f'User {user.id} does not exist!')
            return None
        return salt

    def __cache_token(self, user: User, token: str):
        logger.debug(f"Caching token of User {user.id} for {self.__jwt_ttl} seconds!")
        self.__auth.set(str(user.id + '_token').encode('utf-8'), token, ex=self.__jwt_ttl, nx=True)

    def __get_cached_token(self, user: User):
        cached = self.__auth.get(str(user.id + '_token').encode('utf-8'))
        if cached is not None:
            logger.debug(f"Found cached token of {user.id}!")
        return cached

    def __clear_token_cache(self):
        logger.debug(f"Clearing token cache!")
        cached_keys = self.__auth.keys(str('*_token').encode('utf-8'))
        if len(cached_keys) > 0:
            self.__auth.delete(*cached_keys)

    @staticmethod
    def __hash_password(pwd: str, salt: bytes) -> bytes:
        key = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=pwd.encode('utf-8'),
            salt=salt,
            iterations=100000  # It is recommended to use at least 100,000 iterations of SHA-256
        )
        return key

    def renew_jwt(self, user: User):
        cached = self.__get_cached_token(user)
        # TODO
        pass

    def user_exists(self, user: User):
        return self.__auth.get(user.id) is not None

    def register(self, user: User) -> bool:
        if self.user_exists(user):
            logger.warning(f"User {user.id} already exists!")
            raise HTTPException(status_code=400, detail=f"User {user.id} already exists!")

        salt = self.__store_salt(user)
        logger.debug('Hashing password with PBKDF2')
        key = self.__hash_password(user.password, salt)
        self.__auth.set(user.id, key, nx=True)
        logger.info(f'User {user.id} registered successfully')
        return True

    def authenticate(self, user: User) -> Optional[Dict[str, str]]:
        # get user salt
        salt = self.__get_salt(user)

        # get hashed pw of user
        key = self.__auth.get(user.id)
        if key is None:
            logger.warning(f'User {user.id} does not exist!')
            return None

        # generate new hash from provided pwd
        key2 = self.__hash_password(user.password, salt)

        # check if the two hashes match
        if key == key2:
            # return jwt
            logger.info(f'User {user.id} successfully authenticated!')
            return self.__get_jwt(user)
        else:
            logger.warning(f'Provided password does not match!')
            return None

    def shutdown(self):
        self.__clear_token_cache()
        logger.info('Shutting down AuthHandler!')
