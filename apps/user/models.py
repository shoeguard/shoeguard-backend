from typing import Union

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.db import models

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
        related_name='child',
    )
    parent = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='parent',
    )

    def save(self, *args, **kwargs):
        if self.parent == self.child:
            raise ValueError('Parent and Child must not be the same')
        super(ParentChildPair, self).save(*args, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    phone_number = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=4)
    partner = models.ForeignKey(
        ParentChildPair,
        related_name='partner',
        on_delete=models.PROTECT,
        null=True,
    )

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    @property
    def is_child(self) -> Union[bool, None]:
        if self.partner is None:
            return None
        return self.partner.child == self

    def __str__(self) -> str:
        return self.name
