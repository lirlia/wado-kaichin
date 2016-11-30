# -*- coding: utf-8 -*-

import sys
import os

import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import config as conf
from randomize import rand
from tweet import tweet

dynamodb = boto3.resource(
    'dynamodb',
    region_name= conf.regionName,
    aws_access_key_id=os.getenv("AWS_Access_Key_Id"),
    aws_secret_access_key=os.getenv("AWS_Secret_Access_Key")
)

def Sequence():
    table = dynamodb.Table(conf.tableNameSequence)
    response = table.update_item(
        Key={
             'name': conf.columnNameSequence
        },
        UpdateExpression="set current_number = current_number + :val",
        ExpressionAttributeValues={
        ':val': 1
        },
        ReturnValues="UPDATED_NEW"
    )

    import decimal
    return str(decimal.Decimal(response['Attributes']['current_number']))
#
# DynamoDBに格納されている常用漢字データを取得
#
def GetKanji(num):
    table = dynamodb.Table(conf.tableNameKanji)
    response = table.get_item(
        Key={
             "no": num
        }
    )

    return response['Item']['word']

#
# 指定の条件（１文字目がX、２文字目がX）を
# 満たす熟語を検索
#
def SearchJukugo(word, key, searchFlag):

    table = dynamodb.Table(conf.tableNameJukugo)
    response = table.scan(
        TableName = conf.tableNameJukugo,
        FilterExpression = Key(key).begins_with(word)
    )

    wordList = []
    for i in response['Items']:

        if searchFlag == True:
            if int(i['serchCount']) < conf.searchCount:
                continue

        if key == 'word1':
            wordList.append(i['word2'])

        if key == 'word2':
            wordList.append(i['word1'])

    return wordList

def lambda_handler(event, context):
  #
  # 見つかるまでループ
  #
  while 1:

        # 和同開珎で使用する真ん中の漢字を取得（問題）
        # 以降「人」と表現する
        centerKanji = GetKanji(rand(1, 2136)[0])

        # ?人/人?　を一覧化する
        # frontKeyList: 後ろが人のもの
        # backKeyList: 先頭が人のもの
        frontKeyList = SearchJukugo(centerKanji, 'word2', True)
        backKeyList = SearchJukugo(centerKanji, 'word1', True)

        # 人を使う熟語が1つしか存在しない場合はやり直し
        if len(frontKeyList) < 2 or len(backKeyList) < 2:
            continue

        #
        # 人につながる熟語の片割れの文字をランダムに２個づつ取得する
        #
        frontNum = rand(2, len(frontKeyList))
        backNum = rand(2, len(backKeyList))

        #
        # keyに突っ込む
        #  key1 上の漢字 A人
        #  key2 左の漢字 B人
        #  key3 右の漢字 人C
        #  key4 下の漢字 人D
        #
        key1 = frontKeyList[frontNum[0]]
        key2 = frontKeyList[frontNum[1]]
        key3 = backKeyList[backNum[0]]
        key4 = backKeyList[backNum[1]]

        #
        # A/B/C/Dに共通する文字が
        # 人以外にないかを確認するために
        # それぞれにくっつく文字を取得
        #
        key1JukugoList = SearchJukugo(key1, 'word1', False)
        key2JukugoList = SearchJukugo(key2, 'word1', False)
        key3JukugoList = SearchJukugo(key3, 'word2', False)
        key4JukugoList = SearchJukugo(key4, 'word2', False)

        # 人　以外にないかを確認する
        for key in key1JukugoList:
            if key in key2JukugoList and key in key3JukugoList and key in key4JukugoList:
                if key != centerKanji:
                    continue

        # 問題をTweetする
        tweet(key1, key2, key3, key4, centerKanji, Sequence())
        return { "messages":"success!" }
