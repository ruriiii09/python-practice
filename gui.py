import tkinter
import tkinter.font

def click_btn():
    button["text"] = "クリックしました"

root = tkinter.Tk()
root.title("初めてのボタン")
root.geometry("800x600")
button = tkinter.Button(root,text="ボタンの文字列",
                        font=("Arial",24), command=click_btn)
button.place(x=200,y=100)
root.mainroop()
