import requests # 外部にデータを飛ばすため
import tkinter as tk
from tkinter import messagebox #UI、チェックボックス
from datetime import datetime

def send_report():
    # --- 設定エリア ---
    # ここに発行したWebhook URLを入れる
    WEBHOOK_URL = "https://discord.com/api/webhooks/1475341869201228022/fJhxx7L3-PGtOZXqiRScYJkeYIfMUheyqpHq1aW9zHGX9S0TfNmg0kgLn0jghjU8qDl-"
    
    # --- 入力エリア ---

    # チェックされた項目を回収
    tasks = ["✅ トイレ清掃","✅ 作業場清掃","✅ 冷蔵庫清掃","✅ 墨壺清掃","✅ 床水拭き","✅ 床掃き","✅ amazon発注","✅ フレーバー発注",
    "✅ めいらく発注","✅ スイーツカット","✅ アルミカット","✅ 季節サワー仕込み","✅ 買い出し","✅ ゴミ捨て","✅ ドア、窓拭き","✅ マウピ、おしぼり補充","✅ フレーバー補充"]
    if var1.get(): tasks.append()

    # チェックされた項目を回収
    needs = []
    if var21.get(): needs.append("✅ チーズテリーヌ")
    if var22.get(): needs.append("✅ ショコラテリーヌ")
    if var23.get(): needs.append("✅ パウンドケーキ")
    if var24.get(): needs.append("✅ ブリュレ")
    if var25.get(): needs.append("✅ ウタマロ")
    if var26.get(): needs.append("✅ ハイター")

    
    # 自由記述の内容
    memo = entry_memo.get()
    none_item = input("ないものや買って欲しいもの: ")
    task_str = "\n".join(tasks) if tasks else "特になし"
    need_str = "\n".join(needs) if needs else "特になし"
    now = datetime.now().strftime("%H:%M")

    # --- 報告書の組み立て ---
    report_content = f"""
**【終業報告】** ({now} 報告)
・今日やったこと：{task_str}
・明日やってほしいこと：{need_str}
・ないものや買って欲しいもの：{none_item}
    """

    # --- 送信の魔法 ---
    data = {"content": report_content} # Discord形式
    response = requests.post(WEBHOOK_URL, json=data)

    if response.status_code == 204 or response.status_code == 200:
        print("無事に送信されました。お疲れ様でした。")
    else:
        print(f"おっと、エラーです。ステータスコード: {response.status_code}")

# --- ウィンドウの作成 ---
root = tk.Tk()
root.title("妖精の終業報告ツール")
root.geometry("300x400")

tk.Label(root, text="今日やったことは？", font=("MS Gothic", 12, "bold")).pack(pady=10)

# チェックボックスの変数と設置
i=0
for i in tasks:
   var i+1 = tk.BooleanVar()
   tk.Checkbutton(root, text=tasks[i], variable=var i).pack(anchor="w", padx=20)

var2 = tk.BooleanVar()
tk.Checkbutton(root, text="作業場清掃", variable=var2).pack(anchor="w", padx=20)

var3 = tk.BooleanVar()
tk.Checkbutton(root, text="冷蔵庫清掃", variable=var3).pack(anchor="w", padx=20)

tk.Label(root, text="\nひとことメモ").pack()
entry_memo = tk.Entry(root, width=30)
entry_memo.pack(pady=5)

tk.Button(root, text="報告を送信！", command=send_report, bg="lightblue").pack(pady=20)

root.mainloop()


if __name__ == "__main__":
    send_report()