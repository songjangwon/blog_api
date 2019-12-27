from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from stock.serializers import UserSerializer, GroupSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QEventLoop
from rest_framework import status
import os, sys
from stock.pykiwoom.Kiwoom import *

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def start_pystock(self, request, pk):
        print('ffdfasdfsdf')
        print('123465849')
        app = QApplication(sys.argv)
        kiwoom = Kiwoom()
        kiwoom.comm_connect()
        code_list = kiwoom.get_code_list_by_market('10')

        return Response(code_list, status=status.HTTP_200_OK)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

