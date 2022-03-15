import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from users.models import User


AUTH_HEADER_PREFIX = ['Bearer']

class JWTAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        
        if not auth_header:
            return None
        
        if len(auth_header) == 1:
            return None
        if len(auth_header) > 2:
            return None
        
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')
        
        if prefix not in AUTH_HEADER_PREFIX:
            return None
        
        user = None
        payload = self.deserialize_jwt(token)
        user = User.objects.get(pk=payload.get('user_id'))
        
        if user is None:
            raise exceptions.AuthenticationFailed('No user matching this token was found.')
        
        return user, token
    
    def deserialize_jwt(self, token):
        try:
            return jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=settings.JWT_AUTH.get('JWT_ALGORITHM')
            )
        except:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode token.')