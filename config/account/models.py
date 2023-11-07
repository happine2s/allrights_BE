from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

class UserManager(BaseUserManager):
    def create_user(self, userid, username, password=None):
        if not userid:
            raise ValueError('아이디를 작성해주세요.')
        
        if not username:
            raise ValueError('닉네임을 작성해주세요.')

        user=self.model(
            userid=userid,
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userid, username, password):
        # create_user의 인자와 동일해야함
        user=self.create_user(
            userid,
            username=username,
            password=password
        )
        user.is_admin=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    userid=models.CharField(max_length=30,unique=True)
    username=models.CharField(max_length=30)
    img=models.ImageField(upload_to = "user/", null=True, blank=True)
    bio=models.CharField(max_length=500, blank=True, default='')
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)

    objects=UserManager()

    USERNAME_FIELD='userid'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return self.userid
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin