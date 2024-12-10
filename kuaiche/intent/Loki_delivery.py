#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for delivery

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
INTENT_NAME = "delivery"

userDefinedDICT = {}
try:
    userDefinedDICT = json.load(open(os.path.join(os.path.dirname(__file__), "USER_DEFINED.json"), encoding="utf-8"))
except Exception as e:
    print("[ERROR] userDefinedDICT => {}".format(str(e)))

responseDICT = {}
if CHATBOT_MODE:
    try:
        responseDICT = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "reply/reply_delivery.json"), encoding="utf-8"))
    except Exception as e:
        print("[ERROR] responseDICT => {}".format(str(e)))

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG:
        print("[delivery] {} ===> {}".format(inputSTR, utterance))

def getResponse(utterance, args):
    resultSTR = ""
    if utterance in responseDICT:
        if len(responseDICT[utterance]):
            resultSTR = sample(responseDICT[utterance], 1)[0].format(*args)

    return resultSTR

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern=""):
    debugInfo(inputSTR, utterance)
    if utterance == "哪一家快遞送到香港":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["delivery"] = True
            resultDICT["location"].append(args[24])
            pass

    if utterance == "哪家快遞":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["delivery"] = True
            pass
        
    if utterance == "怎麼配送":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["delivery"] = True
            pass

    if utterance == "怎麼查詢香港的貨態":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["delivery"] = True
            resultDICT["location"].append(args[1])
            pass

    if utterance == "怎麼送到香港":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["delivery"] = True
            resultDICT["location"].append(args[7])
            pass

    if utterance == "用什麼送":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["delivery"] = True
            pass

    if utterance == "用哪一家配送":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["delivery"] = True
            pass

    if utterance == "美國的怎麼查詢貨態":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["delivery"] = True
            resultDICT["location"].append(args[0])
            pass

    if utterance == "貨態":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["delivery"] = True
            pass

    if utterance == "香港的怎麼送":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["delivery"] = True
            resultDICT["location"].append(args[0])
            pass

    if utterance == "香港的訂單用哪家快遞送":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["delivery"] = True
            resultDICT["location"].append(args[0])
            pass

    if utterance == "香港的訂單要怎麼查詢配送狀態":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["delivery"] = True
            resultDICT["location"].append(args[0])
            pass

    return resultDICT