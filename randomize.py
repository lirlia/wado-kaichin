# -*- coding: utf-8 -*-
# 常用漢字の数

import random

def rand(count, max):

    myList = []
    myRange = range(0, max)

    for i in range(0, count):
        tmpRandom = random.randint(0, len(myRange) - 1)

        # ランダム値を配列に格納
        myList.append(myRange[tmpRandom])

        # myRangeからから該当の要素を削除
        myRange.remove(myRange[tmpRandom])

    return myList
