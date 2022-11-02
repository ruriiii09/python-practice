import random
total = 20
d = random.randint(1,6)
y_def = 1
c_def = 1

def banmen():
    print("・"* (y_def -1) + "Y" + "・" *(total - y_def) +"　Goal")
    print("・"* (c_def -1) + "C" + "・" *(total - c_def) +"　Goal")

#banmen()
print("双六スタート！")

while True:
    input("Enterを押すとコマが進みます")
    #print( random.randint(1,6)+  "マス進む")
    y_def = random.randint(1,6) + y_def
    if y_def > total:
        y_def = 20
    elif y_def == 13 or y_def == 19:
        print("残念！ふりだしに戻る！")
        y_def = 1
    elif y_def == 5 or y_def ==10 or y_def == 15:
        print("おめでとう！2マス進む")
        y_def = y_def + 2
    print()
    banmen()
    if y_def == 20:
        print("You Win！")
        break

    input("Enterを押すとCPUのコマが進みます")
    #print( random.randint(1,6) +  "マス進む")
    c_def = random.randint(1,6) + c_def
    if c_def > total:
        c_def = 20
    elif c_def == 13 or c_def == 19:
        print("ふりだしに戻る！")
        c_def = 1
    elif c_def == 5 or c_def == 10 or c_def == 15:
        print("おめでとう！2マス進む")
        c_def = c_def + 2
    banmen()
    if c_def == 20:
        print("You Lose！")
        break