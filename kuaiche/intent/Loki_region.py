#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for region

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
CHATBOT_MODE = False
INTENT_NAME = "region"

userDefinedDICT = {}
try:
    userDefinedDICT = json.load(open(os.path.join(os.path.dirname(__file__), "USER_DEFINED.json"), encoding="utf-8"))
except Exception as e:
    print("[ERROR] userDefinedDICT => {}".format(str(e)))

responseDICT = {}
if CHATBOT_MODE:
    try:
        responseDICT = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "reply/reply_region.json"), encoding="utf-8"))
    except Exception as e:
        print("[ERROR] responseDICT => {}".format(str(e)))

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG:
        print("[region] {} ===> {}".format(inputSTR, utterance))

def getResponse(utterance, args):
    resultSTR = ""
    if utterance in responseDICT:
        if len(responseDICT[utterance]):
            resultSTR = sample(responseDICT[utterance], 1)[0].format(*args)

    return resultSTR

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern=""):
    debugInfo(inputSTR, utterance)
    if utterance == "可以送到香港嗎":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["region"] = True
            resultDICT["location"].append(args[10])
            pass

    if utterance == "運送國家":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["region"] = True
            pass

    if utterance == "配送到府":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["region"] = True
            pass

    if utterance == "香港可以送嗎":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["region"] = True
            resultDICT["location"].append(args[0])
            pass

    if utterance == "香港寄得到嗎":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
            resultDICT["source"] = "reply"
        else:
            resultDICT["region"] = True
            resultDICT["location"].append(args[0])
            pass

    return resultDICT