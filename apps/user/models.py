from __future__ import annotations

from typing import List, Union

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.query import QuerySet

from apps.common.models import BaseModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
        self,
        phone_number,
        name,
        password=None,
    ):
        """
        Creates and saves a User with the given phone_number, name and password.
        """
        if not phone_number:
            raise ValueError('Users must have an phone_number')
        user = self.model(
            phone_number=phone_number,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password):
        """
        Creates and saves a superuser with the given phone_number, name and password.
        """
        user: User = self.create_user(
            phone_number=phone_number,
            name=name,
        )
        user.is_verified = True
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class ParentChildPair(BaseModel):
    child = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='child_pair',
    )
    parent = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='parent_pair',
    )

    def save(self, *args, **kwargs):
        if self.child.partner is not None or self.parent.partner is not None:
            raise ValueError('ParentChildPair already exists.')
        if self.parent == self.child:
            raise ValueError('Parent and Child must not be the same.')

        super(ParentChildPair, self).save(*args, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    phone_number = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=4)
    parent = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        related_name="parent_user",
    )

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    @property
    def is_child(self) -> Union[bool, None]:
        return self.parent is not None

    @property
    def children(self) -> Union[Union[QuerySet[User], List[User]], None]:
        if self.id is None:
            return None
        if self.is_child:
            return None
        return User.objects.filter(parent=self.id)

    def save(self, *args, **kwargs):
        is_parent_self = self.id is not None and self.parent.id == self.id
        if is_parent_self:
            raise ValueError("Parent can't be self")
        return super(User, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
