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
from stock.pykiwoom.kiwoom.Kiwoom import Kiwoom
import os, sys

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    @action(detail=True, methods=['get'])
    def get_code_list(self, request, pk):
        code_list = self.kiwoom.get_code_list_by_market('10')
        return Response(code_list, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def get_account_list(self, request, pk):


        account_num = self.kiwoom.get_account_list()
        return Response(account_num, status=status.HTTP_200_OK)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")


    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)


    def comm_connect(self):

        self.dynamicCall("CommConnect()")

        self.login_event_loop = QEventLoop()

        self.login_event_loop.exec_()



    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

