# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
import os
import sys
import urllib

CK = os.getenv('Twitter_Consumer_Key')                             # Consumer Key
CS = os.getenv('Twitter_Consumer_Secret_Key')         # Consumer Secret
AT = os.getenv('Twitter_Access_Token_Key') # Access Token
AS = os.getenv('Twitter_Access_Token_Secret')         # Accesss Token Secert

#
# tweet
#
def tweet(key1, key2, key3, key4, ans, number):

    # OAuth認証 セッションを開始
    twitter = OAuth1Session(CK, CS, AT, AS)

    # ツイート投稿用のURL
    url = "https://api.twitter.com/1.1/statuses/update.json"

    date = u"[第" + number + u"問目] #わどうかいちん #集計謎\n\n"
    data = date + u"　　　　" + key1 + u"\n\n"
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
