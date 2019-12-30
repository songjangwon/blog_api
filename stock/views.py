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

    @action(detail=True, methods=['get'])
    def test(self, request, pk):
        # # 예수금상세현황요청
        # self.kiwoom.set_input_value("계좌번호", "8127732711")
        # self.kiwoom.set_input_value("비밀번호", "9978")
        # print("예수금상세현황요청1")
        # self.kiwoom.comm_rq_data("예수금상세현황요청", "opw00001", 0, "2000")
        # print("예수금상세현황요청2")
        #
        # # 계좌평가잔고내역요청 - opw00018 은 한번에 20개의 종목정보를 반환
        # self.kiwoom.set_input_value("계좌번호", "8127732711")
        # self.kiwoom.set_input_value("비밀번호", "9978")
        # print("계좌평가잔고내역요청")
        # self.kiwoom.comm_rq_data("계좌평가잔고내역요청", "opw00018", 0, "2000")
        # print("계좌평가잔고내역요청2")
        # item_count = len(self.kiwoom.data_opw00018['stocks'])

        self.kiwoom.set_input_value("계좌번호", "8127732711")
        self.kiwoom.set_input_value("비밀번호", "9978")
        self.kiwoom.comm_rq_data("opw00001_req", "opw00001", 0, "2000")
        print(self.kiwoom.d2_deposit)
        return Response({"das": "das"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def test2(self, request, pk):
        self.kiwoom.set_input_value("계좌번호", "8127732711")
        self.kiwoom.set_input_value("비밀번호", "9978")
        self.kiwoom.comm_rq_data("opw00001_req", "opw00001", 0, "2000")
        print(self.kiwoom.d2_deposit)
        return Response({"das":"das"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def test3(self, request, pk):
        self.kiwoom.test()
        return Response({"das":"das"}, status=status.HTTP_200_OK)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


