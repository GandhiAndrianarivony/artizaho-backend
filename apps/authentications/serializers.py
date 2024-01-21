from datetime import datetime

from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import update_last_login

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUserSession


class CustomTokenObtainSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        # Get token
        refresh = self.get_token(self.user)
        data["refresh_token"] = str(refresh)
        data["access_token"] = str(refresh.access_token)

        # Create session
        session_key = self.create_session()
        active_session = CustomUserSession.objects.filter(
            expires_at__gte=timezone.now(), users=self.user
        )

        # TODO: If needs, we should limited the number of session
        CustomUserSession.objects.create(
            users=self.user,
            session_key=session_key,
            expires_at=datetime.utcfromtimestamp(refresh.get("exp")),
        )

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

    def create_session(self):
        request = self.context["request"]
        session_key = self._create_session_key(request)

        return session_key
    
    @staticmethod
    def _create_session_key(request):
        request.session.create()
        return request.session.session_key
