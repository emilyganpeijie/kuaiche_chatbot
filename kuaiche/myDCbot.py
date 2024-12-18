#!/user/bin/env python
# -*- coding: utf-8 -*-

import logging
import discord
import json
import os
#from dotenv import load_dotenv
from datetime import datetime
from pprint import pprint
from requests import post

from kuaiche import execLoki

#load_dotenv()
logging.basicConfig(level=logging.DEBUG)


def getLokiResult(inputSTR, filterLIST=[]):
    splitLIST = ["！", "，", "。", "？", "!", ",", "\n", "；", "\u3000", ";"] #
    # 設定參考資料
    refDICT = { # value 必須為 list
        #"key": []
    }
    resultDICT = execLoki(inputSTR, filterLIST=filterLIST, splitLIST=splitLIST, refDICT=refDICT)
    logging.debug("Loki Result => {}".format(resultDICT))
    return resultDICT

def llmCall(username, assistantSTR, userSTR):
    url = "https://api.droidtown.co/Loki/Call/" # 中文版
    payload = {
      "username": username,
      "func": "call_llm",
      "data": {
        "model": "Gemma2-9B", # [Gemma2-9B, Llama3-8B]
        "system": "你是一個有耐性的聊天助理。樂於回答任何問題。但你不會特別提起這件事。", # optional
        "assistant": f"回答問題以前，你會仔細考慮以下資訊：{assistantSTR}", # optional
        "user": f"依上文設定，請回答{userSTR}", # required
      }
    }

    llmResult = post(url, json=payload).json()
    print(llmResult)
    return llmResult["result"][0]["message"]["content"]

class BotClient(discord.Client):

    def resetMSCwith(self, messageAuthorID):
        '''
        清空與 messageAuthorID 之間的對話記錄
        '''
        templateDICT = {    "id": messageAuthorID,
                             "updatetime" : datetime.now(),
                             "latestQuest": "",
                             "false_count" : 0
        }
        return templateDICT

    async def on_ready(self):
        # ################### Multi-Session Conversation :設定多輪對話資訊 ###################
        self.templateDICT = {"updatetime" : None,
                             "latestQuest": ""
        }
        self.mscDICT = { #userid:templateDICT
        }
        # ####################################################################################
        print('Logged on as {} with id {}'.format(self.user, self.user.id))

    async def on_message(self, message):
        # Don't respond to bot itself. Or it would create a non-stop loop.
        # 如果訊息來自 bot 自己，就不要處理，直接回覆 None。不然會 Bot 會自問自答個不停。
        if message.author == self.user:
            return None

        logging.debug("收到來自 {} 的訊息".format(message.author))
        logging.debug("訊息內容是 {}。".format(message.content))
        if self.user.mentioned_in(message):
            replySTR = "我是預設的回應字串…你會看到我這串字，肯定是出了什麼錯！"
            logging.debug("本 bot 被叫到了！")
            msgSTR = message.content.replace("<@{}> ".format(self.user.id), "").strip()
            logging.debug("人類說：{}".format(msgSTR))
            if msgSTR == "ping":
                replySTR = "pong"
            elif msgSTR == "ping ping":
                replySTR = "pong pong"

# ##########初次對話：這裡是 keyword trigger 的。
            elif msgSTR.lower() in ["哈囉","嗨","你好","您好","hi","hello"]:
                #有講過話(判斷對話時間差)
                if message.author.id in self.mscDICT.keys():
                    timeDIFF = datetime.now() - self.mscDICT[message.author.id]["updatetime"]
                    #有講過話，但與上次差超過 5 分鐘(視為沒有講過話，刷新template)
                    if timeDIFF.total_seconds() >= 300:
                        self.mscDICT[message.author.id] = self.resetMSCwith(message.author.id)
                        replySTR = "嗨嗨，我們好像見過面，但卓騰的隱私政策不允許我記得你的資料，抱歉！"
                    #有講過話，而且還沒超過5分鐘就又跟我 hello (就繼續上次的對話)
                    else:
                        replySTR = self.mscDICT[message.author.id]["latestQuest"]
                #沒有講過話(給他一個新的template)
                else:
                    self.mscDICT[message.author.id] = self.resetMSCwith(message.author.id)
                    replySTR = "嗨，我是快車肉乾海外客服聊天機器人，\n我們可以為您回答海外配送的相關問題，\n請問您需要什麼協助？"

# ##########非初次對話：這裡用 Loki 計算語意
            else: #開始處理正式對話
                #從這裡開始接上 NLU 模型
                resultDICT = getLokiResult(msgSTR)
                logging.debug("######\nLoki 處理結果如下：")
                logging.debug(resultDICT)
                if resultDICT["source"] == ["LLM_reply"]:
                    assistantSTR = "抱歉，我的資料庫沒有相關的知識，以常識來猜，我會這麼回覆..."
                    userSTR = msgSTR
                    replySTR = llmCall(accountDICT["username"], assistantSTR, userSTR)
                else:
                    replySTR = resultDICT["response"][0]                



                assistantSTR=""
                userSTR = msgSTR
                replySTR = llmCall(accountDICT["username"], assistantSTR, userSTR)

            await message.reply(replySTR)


if __name__ == "__main__":
    with open("account.info", encoding="utf-8") as f: #讀取account.info
            accountDICT = json.loads(f.read())    
    #accountDICT = {"username":"ganpeijie3@gmail.com",
                   #"apikey":"",
                   #"discord_token": os.getenv("discord_token")
                   #}
    client = BotClient(intents=discord.Intents.default())
    client.run(accountDICT["discord_token"])
