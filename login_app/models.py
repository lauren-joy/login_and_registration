from django.db import models
import re
import bcrypt
# Create your models here.
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email address"
        if len(postData['email']) == 0:
            errors["email"] = "Must provide an email"
        current_user = User.objects.filter(email=postData['email'])
        if len(current_user) > 0:
            errors['dulicate'] = "Email already in use"

        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name must be more than 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name must be more than 2 characters"

        if len(postData['password']) < 8:
            errors["password"] = "Password must be more than 8 characters"
        if postData['password'] != postData['pw_confirm']:
            errors['mismatch'] = "Passwords do not match"
        return errors

    def login_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) != 1:
            errors['email'] = "User is nonexistent"
        if len(postData['email']) == 0:
            errors["email"] = "Must provide an email"
        if len(postData['password']) == 0:
            errors["password"] = "Must provide password"
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode())!=True:
            errors['mismatch'] = "Incorrect email and password"
        return errors

class User(models.Model):
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email= models.EmailField()
    password= models.CharField(max_length=60)
    pw_confirm= models.CharField(max_length=60)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects= UserManager()