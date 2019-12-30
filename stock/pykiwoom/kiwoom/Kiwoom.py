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
from pandas import DataFrame
from datetime import datetime
import time
from rest_framework import status
import os, sys



class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()
        # Loop 변수
        # 비동기 방식으로 동작되는 이벤트를 동기화(순서대로 동작) 시킬 때
        self.login_loop = None
        self.request_loop = None
        self.order_loop = None
        self.condition_loop = None

        # 서버구분
        self.server_gubun = None

        # 조건식
        self.condition = None

        # 에러
        self.error = None

        # 주문번호
        self.order_no = ""

        # 조회
        self.inquiry = 0

        # 서버에서 받은 메시지
        self.msg = ""

        # 예수금 d+2
        self.data_opw00001 = 0

        # 보유종목 정보
        self.data_opw00018 = {'account_evaluation': [], 'stocks': []}




    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")


    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self.on_receive_tr_data)
        # self.OnReceiveChejanData.connect(self._receive_chejan_data)
        # self.OnReceiveChejanData.connect(self.on_receive_chejan_data)
        # self.OnReceiveRealData.connect(self.receive_real_data)
        # self.OnReceiveMsg.connect(self.receive_msg)
        # self.OnReceiveConditionVer.connect(self.receive_condition_ver)
        # self.OnReceiveTrCondition.connect(self.receive_tr_condition)
        # self.OnReceiveRealCondition.connect(self.receive_real_condition)


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

    def get_account_list(self):
        account_num = self.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
        account_num = account_num.rstrip(';')
        return account_num

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)


    def comm_rq_data(self, rqname, trcode, next, screen_no):
        print("!!!!!!!!!!!!!!")
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        print("@@@@@@@@@@@@@")
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code,
                               real_type, field_name, index, item_name)
        return ret.strip()
    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def on_receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)
        elif rqname == "opw00001_req":
            self._opw00001(rqname, trcode)
        elif rqname == "opw00018_req":
            self._opw00018(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opw00018(self, rqname, trcode):
        total_purchase_price = self._comm_get_data(trcode, "", rqname, 0, "총매입금액")
        total_eval_price = self._comm_get_data(trcode, "", rqname, 0, "총평가금액")
        total_eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, 0, "총평가손익금액")
        total_earning_rate = self._comm_get_data(trcode, "", rqname, 0, "총수익률(%)")
        estimated_deposit = self._comm_get_data(trcode, "", rqname, 0, "추정예탁자산")

        print(Kiwoom.change_format(total_purchase_price))
        print(Kiwoom.change_format(total_eval_price))
        print(Kiwoom.change_format(total_eval_profit_loss_price))
        print(Kiwoom.change_format(total_earning_rate))
        print(Kiwoom.change_format(estimated_deposit))

    def _opw00001(self, rqname, trcode):
        self.d2_deposit = self._comm_get_data(trcode, "", rqname, 0, "d+2추정예수금")
        print(self.d2_deposit)

    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                         [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])

    def get_chejan_data(self, fid):
        print(fid)
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    def test(self):
        self.set_input_value("계좌번호", "8127732711")
        self.comm_rq_data("opw00018_req", "opw00018", 0, "2000")
