from django.shortcuts import render
from rest_framework.authtoken.models import Token

# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ResetTokenView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        token = Token.objects.get(user=request.user)
        token.delete()
        token = Token.objects.create(user=request.user)
        return Response({
            'token': str(token)
        })