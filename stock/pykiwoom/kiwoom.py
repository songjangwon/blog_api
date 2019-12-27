import os
import sys
from PyQt5.QAxContainer import *
from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import *
# Create your views here.
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from stock.serializers import UserSerializer, GroupSerializer


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

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, request_name, tr_code, inquiry, screen_no):
        """
        키움서버에 TR 요청을 한다.

        조회요청메서드이며 빈번하게 조회요청시, 시세과부하 에러값 -200이 리턴된다.

        :param request_name: string - TR 요청명(사용자 정의)
        :param tr_code: string
        :param inquiry: int - 조회(0: 조회, 2: 남은 데이터 이어서 요청)
        :param screen_no: string - 화면번호(4자리)
        """

        if not self.get_connect_state():
            raise KiwoomConnectError()

        if not (isinstance(request_name, str)
                and isinstance(tr_code, str)
                and isinstance(inquiry, int)
                and isinstance(screen_no, str)):
            raise ParameterTypeError()

        return_code = self.dynamicCall("CommRqData(QString, QString, int, QString)", request_name, tr_code, inquiry,
                                       screen_no)

        if return_code != ReturnCode.OP_ERR_NONE:
            raise KiwoomProcessingError("comm_rq_data(): " + ReturnCode.CAUSE[return_code])

        # 루프 생성: receive_tr_data() 메서드에서 루프를 종료시킨다.
        self.request_loop = QEventLoop()
        self.request_loop.exec_()