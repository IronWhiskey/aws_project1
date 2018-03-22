# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['firstName']) < 2 or len(postData['firstName']) > 255:
            errors["firstName"] = "first name field should not be empty or greater than 255 characters"
        if len(postData['lastName']) < 2 or len(postData['lastName']) > 255:
            errors["lastName"] = "last name field should not be empty"
        if hasNum(postData['firstName']):
            errors['name'] = "first name can not have a number"
        if hasNum(postData['lastName']):
            errors['lastName'] = "last name can not have a number"
        if matchEmail(postData['email']) == False:
            errors['email'] = "Email is not correct format"
        if postData['password'] != postData['confirmPass']:
            errors['password'] = "passwords do not match"
        if len(postData['password']) < 8:
            errors['password'] = "password must be greater than 8 characters"
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


def matchEmail(e):
    return bool(re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', e))

def hasNum(someStr):
    return any(char.isdigit() for char in someStr)