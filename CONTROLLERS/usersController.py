from database import CLIENT
from MODELS.usersModel import userSchema
from cerberus import Validator
import datetime
from copy import deepcopy
import json
from flask import jsonify
import bcrypt

VALIDATE = Validator(require_all=True).validate
USER = CLIENT['user']


def cryptography(pwd):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd.encode(), salt)
    return hashed


def registerController(data):
    dataWithoutDate = deepcopy(data)
    data['date'] = datetime.datetime.utcnow()
    data['pwd'] = cryptography(data['pwd']).decode("utf-8")
    if VALIDATE(data, userSchema) == True:
        email = [user['email'] for user in usersController()[0]]
        if data['email'] not in email:
            USER.insert_one(data)
            return dataWithoutDate, 201
        else:
            return {"message": "Email already exists"}, 400
    else:
        return {"error": "Invalid data"}, 400


def usersController():
    users = []
    for user in USER.find():
        user['_id'] = str(user['_id'])
        users.append(user)

    return users, 200
