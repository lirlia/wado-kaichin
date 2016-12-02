# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
import os
import sys
import urllib
import config as conf

CK = os.getenv('Twitter_Consumer_Key')                             # Consumer Key
CS = os.getenv('Twitter_Consumer_Secret_Key')         # Consumer Secret
AT = os.getenv('Twitter_Access_Token_Key') # Access Token
AS = os.getenv('Twitter_Access_Token_Secret')         # Accesss Token Secert

def difficulty(num):
    if 0 <= num  < 5000:
        return "★★★★★"
    if 5000 < num  < 30000:
        return "★★★★☆"
    if 30000 < num  < 80000:
        return "★★★☆☆"
    if 80000 < num  < 200000:
        return "★★☆☆☆"
    if 200000 < num:
        return "★☆☆☆☆"
#
# tweet
#
def tweet(key1, key2, key3, key4, ans, number, searchCountAmount):

    # OAuth認証 セッションを開始
    twitter = OAuth1Session(CK, CS, AT, AS)

    # ツイート投稿用のURL
    url = "https://api.twitter.com/1.1/statuses/update.json"

    data = u"[第" + number + u"問目] \n"
    data = data + "#わどうかいちん #解けたらRT #集計謎\n\n"
    data = data + u"難易度（目安）:" + difficulty(searchCountAmount) + "\n\n"
    data = data + u"　　　　" + key1 + u"\n\n"
    data = data + u"　　　　⬇️\n\n"
    data = data + key2 + u"　➡️　？　➡️　" + key3 + u"\n"
    data = data + u"　　　　⬇️\n\n"
    data = data + u"　　　　" + key4 + u"\n\n"
    data = data + u"\n▼解答はこちら\n"
    data = data + u"http://www.weblio.jp/content/" + urllib.quote_plus(ans.encode('utf-8')) + "?dictCode=KNJJN"

    # ツイート本文
    params = {"status": data}

    # OAuth認証で POST method で投稿
    req = twitter.post(url, params = params)

    # レスポンスを確認
    if req.status_code == 200:
        print ("OK")
    else:
        print ("Error: %d" % req.status_code)
        sys.exit()
