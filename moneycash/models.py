# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    empresa = models.ForeignKey('Empresa', null=True,
        related_name="empresa_usuario")

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_empresa(self):
        if self.empresa:
            return True
        else:
            return False

    def get_empresa(self, name=''):
        if not self.empresa:
            e, create = Empresa.objects.get_or_create(razon_social=name,
                administrador=self)
        else:
            e = self.empresa
        return e

    def is_admistrador(self):
        if self.empresa and self.empresa.administrador == self:
            return True
        else:
            return False

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Empresa(models.Model):
    razon_social = models.CharField(max_length=255,
        verbose_name="nombre de la empresa", null=True)
    numero_ruc = models.CharField(max_length=14,
        verbose_name="registro unico del contribuidor (RUC)", null=True)
    direccion = models.CharField(max_length=255,
        verbose_name="direccion de la empresa", null=True)
    telefono = models.CharField(max_length=14,
        verbose_name="numero de telefono", null=True)
    email = models.CharField(max_length=255,
        verbose_name="correo electronico", null=True)
    web = models.CharField(max_length=14,
        verbose_name="sitio web", null=True)
    administrador = models.ForeignKey(MyUser, null=True,
        related_name="empresa_administrador")
