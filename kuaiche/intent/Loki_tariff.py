#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for tariff

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
INTENT_NAME = "tariff"

userDefinedDICT = {}
try:
    userDefinedDICT = json.load(open(os.path.join(os.path.dirname(__file__), "USER_DEFINED.json"), encoding="utf-8"))
except Exception as e:
    print("[ERROR] userDefinedDICT => {}".format(str(e)))

responseDICT = {}
if CHATBOT_MODE:
    try:
        responseDICT = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "reply/reply_tariff.json"), encoding="utf-8"))
    except Exception as e:
        print("[ERROR] responseDICT => {}".format(str(e)))

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG:
        print("[tariff] {} ===> {}".format(inputSTR, utterance))

def getResponse(utterance, args):
    resultSTR = ""
    if utterance in responseDICT:
        if len(responseDICT[utterance]):
            resultSTR = sample(responseDICT[utterance], 1)[0].format(*args)

    return resultSTR

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern=""):
    debugInfo(inputSTR, utterance)
    if utterance == "入境的話會有需要支付額外的費用嗎":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["tariff"] = True
            pass

    if utterance == "入境的話還會有需要另外付錢嗎":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["tariff"] = True
            pass

    if utterance == "寄到香港的費用":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["tariff"] = True
            resultDICT["location"].append(args[7])
            pass

    if utterance == "送到香港如何計費":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["tariff"] = True
            resultDICT["location"].append(args[10])
            pass

    if utterance == "送到香港的話還會有要另外付錢嗎":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["tariff"] = True
            pass

    if utterance == "送到香港要多少錢":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["tariff"] = True
            resultDICT["location"].append(args[8])
            pass

    if utterance == "關稅":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["tariff"] = True
            pass

    return resultDICT