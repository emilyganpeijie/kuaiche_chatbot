#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for payment

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict,
        refDICT       dict,
        pattern       str

    Output:
        resultDICT    dict
"""

from random import sample
import json
import os

DEBUG = True
CHATBOT_MODE = True
INTENT_NAME = "payment"

userDefinedDICT = {}
try:
    userDefinedDICT = json.load(open(os.path.join(os.path.dirname(__file__), "USER_DEFINED.json"), encoding="utf-8"))
except Exception as e:
    print("[ERROR] userDefinedDICT => {}".format(str(e)))

responseDICT = {}
if CHATBOT_MODE:
    try:
        responseDICT = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "reply/reply_payment.json"), encoding="utf-8"))
    except Exception as e:
        print("[ERROR] responseDICT => {}".format(str(e)))

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG:
        print("[payment] {} ===> {}".format(inputSTR, utterance))

def getResponse(utterance, args):
    resultSTR = ""
    if utterance in responseDICT:
        if len(responseDICT[utterance]):
            resultSTR = sample(responseDICT[utterance], 1)[0].format(*args)

    return resultSTR

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern=""):
    debugInfo(inputSTR, utterance)
    if utterance == "ApplePay可以用來付款":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["payment"] = True
            resultDICT["pMethod"].append(args[2])
            pass

    if utterance == "付款方式":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["payment"] = True
            pass

    if utterance == "信用卡":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["payment"] = True
            resultDICT["pMethod"].append(args[1])
            pass

    if utterance == "信用卡付款":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["payment"] = True
            resultDICT["pMethod"].append(args[1])
            pass

    if utterance == "可以怎麼付款":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["payment"] = True
            resultDICT["pMethod"].append(args[4])
            pass

    if utterance == "支付可以用":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["payment"] = True
            resultDICT["pMethod"].append(args[10])
            pass

    if utterance == "有ApplePay嗎":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["payment"] = True
            resultDICT["pMethod"].append(args[15])
            pass

    return resultDICT