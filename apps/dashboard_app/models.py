from __future__ import unicode_literals
from django.db import models
import re
# from django.core.exceptions import ValidationError
# from django.core.validators import validate_email

class LogManager(models.Manager):
    def log_validator(postData):
        errors = {}
        if len(postData['email']) < 1:
            errors["email"] = "Please use correct email address"
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", postData['email']):
            errors["valid_email"] = "Please use correct email form"
        if len(postData['pass_word']) < 1:
            errors["pass"] = "Password too short"
        return errors

class UserManager(models.Manager):
    def regi_validator(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors["fname"] = "Entered first name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "Entered last name should be at least 2 characters"
        if len(postData['email']) < 2:
            errors["email"] = "Please use correct email address"
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", postData['email']):
            errors["valid_email"] = "Please use correct email form"
        if len(postData['pass_word']) < 2:
            errors["pass"] = "Password too short"
        if postData['pass_word'] != postData['confirm_password']:
            errors["pass"] = "Password doesn't match"
        if User.objects.filter(email_address=postData['email']):
            errors["email_exists"] = "Email exists"
        return errors
    
    def user_edit_validator(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors["fname"] = "Entered first name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "Entered last name should be at least 2 characters"
        if len(postData['email']) < 2:
            errors["email"] = "Please use correct email address"
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", postData['email']):
            errors["valid_email"] = "Please use correct email form"
        list = User.objects.exclude(id=int(postData['uid']))
        if list.filter(email_address=postData['email']):
            errors["email_exists"] = "Email exists"
        return errors
    
class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['author']) < 4:
            errors["author"] = "Author name should be more then 3 characters"
        if len(postData['quote']) < 11:
            errors["quote"] = "Message should be more then 10 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email_address = models.CharField(max_length=255)
    pass_word = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class Quote(models.Model):
    author = models.CharField(max_length=100)
    quotes = models.TextField()
    quoted_by = models.ForeignKey(User, related_name="quotes")
    liked_by = models.ManyToManyField(User, related_name="liked_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
    
    