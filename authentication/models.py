# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import jwt
from django.db import models
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager
)
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from utils.models import BaseAbstractModel
from django.conf import settings
from datetime import datetime, timedelta
from utils.managers import CustomQuerySet


class UserManager(BaseUserManager):
    """
    we need to overide the create user field so that users can be created only when 
    all non nullable fields are populated
    """

    def create_user(self, first_name, last_name, email, password, role="PH"):
        """
        create a user and return fields with first name, email and password
        """
        if not first_name:
            raise TypeError("Users must have a first nae")
        if not email:
            raise TypeError("users must have an email")
        if not last_name:
            raise TypeError("users must have a last")
        if not password:
            raise TypeError("users must have a password")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=self.normalize_email(email),
        )
        user.set_password(password)
        user.role = role

        user.save()
        return user

    def create_superuser(
            self, first_name=None, last_name=None, email=None, password=None):
        """Create a `User` who is also a superuser"""
        if not first_name:
            raise TypeError('Superusers must have a first name.')

        if not last_name:
            raise TypeError('Superusers must have a last name.')

        if not email:
            raise TypeError('Superusers must have an email address.')

        if not password:
            raise TypeError('Superusers must have a password.')

        user = self.model(
            first_name=first_name, last_name=last_name,
            email=self.normalize_email(email), role='GO')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.is_verified = True
        user.set_password(password)
        user.save()


class User(AbstractUser, BaseAbstractModel):
    """ this class defines the user model """
    USER_ROLES = (
        ("PH", "PHARMACIST"),
        ("PT", "PATIENT"),
        ("GO", "GOVERNMENT OFFICIAL")
    )

    username = models.CharField(
        null=True, blank=True, max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        verbose_name="user role", max_length=2, choices=USER_ROLES, default="PH"
    )
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()
    active_objects = CustomQuerySet.as_manager()

    def __str__(self):
        return f'{self.email}'

    @property
    def get_email(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first and last name. Since we do
        not store the user's real name, we return their emails instead.
        """
        return self.email

    @property
    def token(self):
        """
        We need to make the method for creating our token private. At the
        same time, it's more convenient for us to access our token with
        `user.token` and so we make the token a dynamic property by wrapping
        in in the `@property` decorator.
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        We generate JWT token and add the user id, username and expiration
        as an integer.
        """
        token_expiry = datetime.now() + timedelta(hours=24)

        token = jwt.encode({
            'id': self.pk,
            'email': self.get_email,
            'exp': int(token_expiry.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
