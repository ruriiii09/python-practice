import random
import datetime
alp = ["A","B","C","D","E","F","G",
"H","I","J","K","L","M","N",
"O","P","Q","R","S","T","U",
"V","W","X","Y","Z"]
r = random.choice(alp)
a = ""

for i in alp:
    if i != r:
        #何も入ってない箱にA〜Gまで入力
        a = a + i
print(a)
st = datetime.datetime.now()

ans = input("抜けているアルファベットは？")
if ans == r :
    print("正解です")
    et = datetime.datetime.now()
    print("回答までのタイム：" + str((et-st).seconds))
else:
    print("不正解です")
