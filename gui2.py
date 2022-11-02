import tkinter
import random
from PIL import Image, ImageTk

a = ["大吉 \n好きな相手との間に今まで以上の \n深いつながりを生み出す絶好のチャンス！",
     "大吉 \n自分を信じて成果のでる日となりそうです。 \n人目を気にせず、自分を大切にしましょう。",
     "中吉 \n混乱していたことも解決できる一日になりそうです。",
     "中吉 \n頭の回転が速く、誰も思いつかないようなことをヒラメキそう。",
     "吉 \nインスピレーションだけで行動するには少々運気が弱い一日。",
     "吉 \n集中して一気に終わらせるよりも、同じペースで継続し続けることで \n新しい自分が発見できる一日です。",
     "小吉 \n時の流れに身をゆだねてみると運気がアップしそうな日です。",
     "小吉 \nひとりで頑張ろうとせず、年長者の後押しを頼みましょう。",
     "凶 \n疲れやストレスがたまってダウン寸前！ \nハーブやアロマオイルを試してみたりするといいかも。",
     "凶 \nやりたいことはいっぱいあるのですが、体力が伴わない運勢です。 \n自分を主張せず、みんなの引き立て役に回って。",
     "大凶 \n好きな相手とのトラブルが多い一日とも言えます。 \nもっと、寄り添う努力を重ねて冷静に立ち回ってみて。",
     "大凶 \nズルズルと先送りにしてきたことが、 \n大きな問題を引き起こす暗示があります。 \n現実を見据えて決断を下しましょう。"]

#クリック後の動作を定義
def click_btn():
    label["text"] = str(random.choice(a))
    button["text"] = "再チャレンジする？"

root = tkinter.Tk()
root.title("tkinter practice")
root.geometry("700x500")


#文字を表示する
label = tkinter.Label(root,text = "おみくじスタート！",
                      font=("AsobiMemogaki",25))
#label.place(x=200,y=100)
label.pack(anchor='center',expand=1)

#rootウィンドウの中にtextの書かれたボタンを配置して、コマンドにクリック後の動作を実行する
button = tkinter.Button(root, text="おみくじを引く",
                        font=("AsobiMemogaki",40),command=click_btn)
#button.place(x=400, y=300)
button.pack(anchor='center',expand=1)
#command=click_btn()

#canvas = tkinter.Canvas(root,width=1000,height=600)
#canvas.pack()
#backgroundImage=root.PhotoImage("programing\python games\0001.png") 



root.mainloop()
