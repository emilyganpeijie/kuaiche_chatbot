#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from random import choice
from requests import post
from time import sleep
import json
import os


BASE_PATH = os.path.dirname(os.path.abspath(__file__))

accountDICT = {}
try:
    dataDICT = json.load(open(os.path.join(os.path.dirname(BASE_PATH), "account.info"), encoding="utf-8"))
    keyLIST = ["username", "loki_key"]
    if all(key in dataDICT for key in keyLIST):
        if all(dataDICT[key] for key in keyLIST):
            if all(type(dataDICT[key]) == str for key in keyLIST):
                accountDICT = {key: dataDICT[key] for key in keyLIST}
except Exception as e:
    print(f"[ERROR] account.info => {str(e)}")

ragDICT = {}
try:
    dataDICT = json.load(open(os.path.join(BASE_PATH, "RAG.config"), encoding="utf-8"))
    keyLIST = ["username", "copytoaster_key", "category"]
    if all(key in dataDICT for key in keyLIST):
        if dataDICT["username"] and dataDICT["copytoaster_key"] and dataDICT["category"]:
            if type(dataDICT["username"]) == str and type(dataDICT["copytoaster_key"]) == str and type(dataDICT["category"]) == list:
                if dataDICT["category"] and all(type(category) == str for category in dataDICT["category"]):
                    ragDICT = {
                        "username": dataDICT["username"],
                        "copytoaster_key": dataDICT["copytoaster_key"],
                        "category": dataDICT["category"]
                    }
except Exception as e:
    print(f"[ERROR] RAG.config => {str(e)}")

llmDICT = {}
try:
    dataDICT = json.load(open(os.path.join(BASE_PATH, "LLM.config"), encoding="utf-8"))
    keyLIST = ["intent", "system", "prompt"]
    if all(key in dataDICT for key in keyLIST):
        if all(dataDICT[key] for key in keyLIST):
            if all(type(dataDICT[key]) == str for key in keyLIST):
                llmDICT = {key: dataDICT[key] for key in keyLIST}

    llmDICT["header"] = []
    if "header" in dataDICT and type(dataDICT["header"]) == list and dataDICT["header"]:
        if all(type(header) == str for header in dataDICT["header"]):
            llmDICT["header"] = dataDICT["header"]
except Exception as e:
    print(f"[ERROR] LLM.config => {str(e)}")


def askCopyToaster(inputSTR, count=3):
    resultLIST = []
    if ragDICT:
        url = "https://api.droidtown.co/CopyToaster/API/V2/"
        payload = {
            "username": ragDICT["username"],
            "copytoaster_key": ragDICT["copytoaster_key"],
            "input_str": inputSTR,
            "count": count
        }

        for category in ragDICT["category"]:
            payload["category"] = category
            while True:
                try:
                    response = post(url, json=payload).json()
                    if response["status"]:
                        if response["progress_status"] == "completed":
                            for r in response["result_list"]:
                                resultLIST.append(r["document"].split(">>\\n")[1])
                                break
                    else:
                        print(f"[askCopyToaster] Project: {ragDICT['project']}, Category: {category} => {response['msg']}")
                        break
                except Exception as e:
                    print(f"[askCopyToaster] {str(e)}")
                    break

                sleep(1.2)

    return resultLIST

def askLLM(inputSTR, referenceSTR=""):
    responseSTR = ""
    sourceSTR = ""
    if accountDICT and llmDICT:
        url = "https://api.droidtown.co/Loki/Call/"
        payload = {
            "username": accountDICT["username"],
            "loki_key": accountDICT["loki_key"],
            "intent": llmDICT["intent"],
            "func": "run_alias",
            "data": {
                "messages": [
                    {"role": "system", "content": llmDICT["system"]}
                ]
            }
        }
        headerSTR = ""
        if referenceSTR and type(referenceSTR) == str:
            sourceSTR = "RAG_reply"
            payload["data"]["messages"].append({"role": "user", "content": llmDICT["prompt"].replace("{{INPUT}}", inputSTR)})
        else:
            sourceSTR = "LLM_reply"
            try:
                headerSTR = choice(llmDICT["header"])
            except:
                headerSTR = "我的資料庫沒有相關的資料，但網路資料顯示..."

            payload["data"]["messages"].append({
                "role": "user",
                "content": f"You will use the facts below as reference and only the facts below:\n{referenceSTR}\n {llmDICT['prompt'].replace('{{INPUT}}', inputSTR)}"
            })

        try:
            result = post(url, json=payload).json()
            if result["status"]:
                if headerSTR:
                    responseSTR = f'{headerSTR}\n{result["result_list"][0]["message"]["content"]}'
                else:
                    responseSTR = result["result_list"][0]["message"]["content"]
            else:
                print(f"[askLLM] {result['msg']}")
        except Exception as e:
            print(f"[askLLM] {str(e)}")

    return responseSTR, sourceSTR

def callLLM(inputSTR):
    copyToasterResultLIST = askCopyToaster(inputSTR)
    if copyToasterResultLIST:
        referenceSTR = "\n".join(copyToasterResultLIST)
    else:
        referenceSTR = ""

    llmResultSTR, sourceSTR = askLLM(inputSTR, referenceSTR=referenceSTR)
    return llmResultSTR, sourceSTR


if __name__ == "__main__":
    inputSTR = "今天天氣如何？"
    resultSTR, sourceSTR = callLLM(inputSTR)
    print(sourceSTR)
    print(resultSTR)