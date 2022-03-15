import jwt
from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from rest_framework_jwt.settings import api_settings
from conf.models import BaseModel, SoftDeleteModel


# 유저를 생성할 때 사용하는 헬퍼(Helper) 클래스
class UserManager(BaseUserManager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(UserManager, self).__init__(*args, **kwargs)
    
    def get_queryset(self):
        if not self.alive_only:
            return super().get_queryset()
        return super().get_queryset().filter(deleted_at__isnull=True)
    
    def create_user(self, email, name, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(email=self.normalize_email(email), name=name, **kwargs)
        user.set_password(password)
        # settings.py에서 기본으로 설정한 db에 저장
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password):
        user = self.create_user(email=email, password=password, name=name,)
        user.is_staff = True
        user.save(using=self._db)
        return user

# 실제 모델
class User(AbstractBaseUser, BaseModel, SoftDeleteModel):
    email = models.EmailField('이메일', max_length=255, unique=True)
    name = models.CharField('이름', max_length=100)
    is_staff = models.BooleanField('직원유무',  default=False)
    is_active = models.BooleanField('활성 여부', default=False)
    
    # 장고에서 모든 모델은 manager을 가지고 있으나, 다른 manager을 사용할 때는 objects로 선언
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = [
        'name',
    ]
    
    class Meta:
        db_table = 'users'
        ordering = ['-id']
    
    # property: 메소드를 마치 필드인 것처럼 취급 
    # 즉, User.token() 이 아니라 User.token으로 불러옴
    @property
    def token(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        payload = jwt_payload_handler(self)
        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.JWT_AUTH.get('JWT_ALGORITHM')
        )
        return token.decode()
        