q = ["1＋1は？","4×3は？","12÷2は？"]
a = ["2","12","6"]
aa = ["２","１２","６"]

for i in range(3):
    print(q[i])
    ans = input()
    if ans == a[i] or ans == aa[i]:
        print("正解です")
    else:
        print("不正解です")