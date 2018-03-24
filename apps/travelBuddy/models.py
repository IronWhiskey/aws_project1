# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import datetime

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['firstName']) < 2 or len(postData['firstName']) > 255:
            errors["firstName"] = "first name field should not be empty or greater than 255 characters"

        if len(postData['lastName']) < 2 or len(postData['lastName']) > 255:
            errors["lastName"] = "last name field should not be empty"

        if hasNum(postData['firstName']):
            errors['lastname'] = "first name can not have a number"
            
        if hasNum(postData['lastName']):
            errors['lastName'] = "last name can not have a number"

        if postData['password'] != postData['confirmPass']:
            errors['password'] = "passwords do not match"

        if len(postData['password']) < 8:
            errors['password'] = "password must be greater than 8 characters"

        return errors


class TripManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        today = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")
        print today
        if len(postData['destination']) < 2:
            errors["destination"] = "destination field should not be less than 2 characters"
        
        if len(postData['destination']) > 255:
            errors["destination"] = "destination field should not be greater 255 characters"

        if len(postData['description']) < 2 or len(postData['description']) > 255:
            errors["description"] = "description field should not be empty or less than 2 characters"

        if len(postData['travel_start']) == 0:
            errors["travel_start"] = "travel_start field should not be empty"
        
        if len(postData['travel_end']) == 0:
            errors["travel_end"] = "travel_end field should not be empty"

        if (postData['travel_start'] < today):
            errors["travel_end"] = "travel_start date must be equal or greater than todays date"
        
        if (postData['travel_start'] > postData['travel_end']):
            errors["travel_end"] = "travel_end field must be after travel start field"

        
        return errors   


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Trip(models.Model):
    attendee = models.ManyToManyField(User, related_name="trips")
    planner = models.ForeignKey(User, related_name='trip')
    travel_start = models.DateTimeField()
    travel_end = models.DateTimeField()
    description = models.TextField()
    destination = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()

def matchEmail(e):
    return bool(re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', e))

def hasNum(someStr):
    return any(char.isdigit() for char in someStr)