import streamlit as st
import gspread
import sqlite3
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime
import re

if 'val_new' not in st.session_state: st.session_state.val_new = 0
if 'val_repeat' not in st.session_state: st.session_state.val_repeat = 0
if 'all_customer' not in st.session_state: st.session_state.all_customer = 0

#dt_year = datetime.now().year
#dt_month = datetime.now().month
dt_day = datetime.now().day
cell_new = ""
cell_repeat = ""
all_customer = 0

# --- 1. データベースの初期設定（カラムを拡張） ---
def init_db():
    conn = sqlite3.connect('my_business_log.db', check_same_thread=False)
    c = conn.cursor()
    # カラムを具体的に定義して作成
    c.execute('''CREATE TABLE IF NOT EXISTS daily_reports_v2 
                 (report_date TEXT, 
                  report_type TEXT, 
                  content TEXT, 
                  done_items TEXT, 
                  next_items TEXT, 
                  buy_items TEXT, 
                  names TEXT, 
                  cat1 TEXT, 
                  cat2 TEXT, 
                  cat3 TEXT, 
                  created_at TEXT)''')
    conn.commit()
    return conn

conn = init_db()
# --- 2. 保存関数をアップデート ---
def save_report(r_date, r_type, content, data_dict):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c = conn.cursor()
    c.execute('''INSERT INTO daily_reports_v2
                 (report_date, report_type, content, done_items, next_items, buy_items, names, cat1, cat2, cat3, created_at) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (r_date, r_type, content, 
               ",".join(data_dict['done']), ",".join(data_dict['next']), ",".join(data_dict['buy']),
               data_dict['names'], data_dict['cat1'], data_dict['cat2'], data_dict['cat3'], now))
    conn.commit()

# --- 3. セッション状態の初期化（ここが自動転記の鍵） ---
# keyで指定する変数をあらかじめ作っておく
input_keys = {
    'done': [], 'next': [], 'buy': [], 
    'names_input': "", 'cat1_val': "", 'cat2_val': "", 'cat3_val': ""
}
for k, v in input_keys.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- 3. データを読み込む関数 ---
def load_reports(selected_date):
    query = "SELECT report_type, content, created_at FROM daily_reports_v2 WHERE report_date = ?"
    return pd.read_sql(query, conn, params=(selected_date,))

# --- データベース接続関数 ---
def get_db_conn():
    return sqlite3.connect('my_business_log.db', check_same_thread=False)

# --- 最新の中間報告の「数値や状態」をバラバラに取得する関数 ---
def get_latest_mid_data():
    conn = get_db_conn()
    today = str(datetime.now().date())
    # 今日の中間報告のうち、一番新しい1件を取得
    query = "SELECT report_type, content, created_at FROM daily_reports_v2 WHERE report_date = ? AND report_type = '中間' ORDER BY created_at DESC LIMIT 1"
    try:
        df = pd.read_sql(query, conn, params=(today,))
        if not df.empty:
            return df.iloc[0].to_dict() # 辞書形式で返す
    except:
        pass
    return None

# --- 1. Google Sheets 連携設定 ---
def get_worksheet():
    # --- 1. 接続の準備（これは共通） ---
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file('secrets.json', scopes=scope)
    client = gspread.authorize(creds)
    
   # スプレッドシートとワークシートを開く
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1VcxqJkEXOb7Hh8YSrElekjiGlDSUVe5S7Q2OFVLo2NE/edit?usp=sharing"
    sh = client.open_by_url(SHEET_URL)
    ws =sh.worksheet("データ")


    # 3. 指定した数字を含むセルを検索
    cell = ws.cell(2,dt_day+1)
    
    # 4. その下のセル(行を+1)を取得 グローバル化
    # セルの値を数値として取得（空なら0にする）
    raw_new = ws.cell(cell.row + 2, cell.col).value
    raw_repeat = ws.cell(cell.row + 3, cell.col).value
        
    # 安全に数値変換
try:
    val_new = int(raw_new) if raw_new and str(raw_new).isdigit() else 0
    val_repeat = int(raw_repeat) if raw_repeat and str(raw_repeat).isdigit() else 0
    all_customer = st.session_state.val_new + st.session_state.val_repeat
except Exception as e:
    st.error(f"取得エラー: {e}")
    

# --- 2. 報告書成形用ヘルパー ---
def format_items(selected, added):
    items = [f"{item}" for item in selected]
    if added:
        items.append(f"{added}")
    return "\n".join(items) if items else "なし"

# --- 3. アプリ設定 ---
st.set_page_config(page_title="終業報告アプリ", layout="wide")
st.title("終業報告アプリ")

# --- サイドバー：まず人数を記録 ---
st.sidebar.header("📊 ステップ1：人数記録")

if st.sidebar.button("スプシから取得"):
    try:
        ws = get_worksheet()
        now_date = datetime.now().strftime("%Y/%m/%d")
        st.sidebar.text(f"新規：{val_new}名")
        st.sidebar.text(f"リピーター：{val_repeat}名")
        st.sidebar.text(f"計：{all_customer}名")
    except Exception as e:
        st.error(f"まだ人数が入力されていません: {e}")
#ws.append_row([now_date, visitor_count])
#st.sidebar.success(f" の人数を記録したよ！")

# --- サイドバー：カレンダーと履歴 ---
st.sidebar.title("📅 過去の報告を確認")
view_date = st.sidebar.date_input("日付を選択", datetime.now().date())
history_df = load_reports(str(view_date))

if not history_df.empty:
    st.sidebar.write(f"--- {view_date} の記録 ---")
    for i, row in history_df.iterrows():
        with st.sidebar.expander(f"{row['report_type']} ({row['created_at'][11:16]})"):
            st.caption(row['content'])
else:
    st.sidebar.info("この日の記録はありません。")
    

        
# --- メイン画面：ステップ2：報告内容入力 ---
st.header("📋 報告事項の入力")
cat4 = st.text("月：めいらく発注 --- 火：可燃、ダンボ（第1,3は全部捨てる） --- 水：床水拭き --- 金：可燃、ダンボ")
col1, col2, col3 = st.columns(3)

# --- 4. 自動転記ボタンの処理 ---
def sync_mid_report():
    today = str(datetime.now().date())
    query = "SELECT * FROM daily_reports_v2 WHERE report_date = ? AND report_type = '中間' ORDER BY created_at DESC LIMIT 1"
    df = pd.read_sql(query, conn, params=(today,))
    
    if not df.empty:
        res = df.iloc[0]
        try:
            st.session_state.done = res['done_items'].split(",") if res.get('done_items') else []
            st.session_state.next = res['next_items'].split(",") if res.get('next_items') else []
            st.session_state.buy = res['buy_items'].split(",") if res.get('buy_items') else []
            st.session_state.names_input = res.get('names', "")
            st.session_state.cat1_val = res.get('cat1', "")
            st.session_state.cat2_val = res.get('cat2', "")
            st.session_state.cat3_val = res.get('cat3', "")
            st.success("中間報告から転記しました！")
        except KeyError as e:
            st.error(f"データベースの構造が古いようです。ファイルを削除してやり直してください: {e}")
    else:
        st.warning("今日の中間報告は見つかりませんでした。")

# 2. 終業報告の入力欄
tab1, tab2 = st.tabs(["📝 報告入力", "📅 過去ログ"])

with tab1:
    # ステップ1：人数取得
    with st.expander("📊 ステップ1：スプシから人数同期", expanded=False):
        if st.button("スプレッドシートから取得", use_container_width=True):
            try:
                ws = get_worksheet()
                now_date = datetime.now().strftime("%Y/%m/%d")
            except Exception as e:
                st.error(f"まだ人数が入力されていません: {e}")
            st.info(f"同期完了（新規：{cell_new.value or 0}名 / リピーター：{cell_repeat.value or 0}名 計：{all_customer}名）") 

    # 自動転記ボタン（目立つように配置
    st.button("📋 中間報告の内容を自動入力", on_click=sync_mid_report, use_container_width=True)
with tab2:
    st.subheader("📅 履歴検索")
    search_date = st.date_input("確認したい日", datetime.now().date())
    # SQLで読み込み
    query = "SELECT * FROM daily_reports_v2 WHERE report_date = ?"
    history_df = pd.read_sql(query, conn, params=(str(search_date),))
    
    if not history_df.empty:
        for _, row in history_df.iterrows():
            with st.expander(f"{row['report_type']} ({row['created_at'][11:16]})"):
                st.text(row['content'])
    else:
        st.info("記録がありません。")

# --- 設定：スマホで見た時にサイドバーが邪魔にならないよう調整 ---
st.set_page_config(page_title="Mosh Report", layout="centered", initial_sidebar_state="collapsed")
        
st.subheader("📋 報告事項")
    
# スマホでは1カラムずつにするため、columnsを使わず縦に並べるか、小分けにする
done_items = st.multiselect("今日やったこと", ["・トイレ清掃","・作業場清掃","・冷蔵庫清掃","・墨壺清掃","・床水拭き","・床掃き","・amazon発注","・フレーバー発注","・めいらく発注","・スイーツカット","・アルミカット","・季節サワー仕込み","・買い出し","・ゴミ捨て","・ドア、窓拭き","・マウピ、おしぼり補充","・フレーバー補充"], key="done")
done_add = st.text_area("追記（はじめに・をつけてね）", key="done_a")
next_items = st.multiselect("明日やってほしいこと", ["・トイレ清掃","・作業場清掃","・冷蔵庫清掃","・墨壺清掃","・床水拭き","・床掃き","・amazon発注","・フレーバー発注","・めいらく発注","・スイーツカット","・アルミカット","・季節サワー仕込み","・買い出し","・ゴミ捨て","・ドア、窓拭き","・マウピ、おしぼり補充","・フレーバー補充"], key="next")
next_add = st.text_area("追記（はじめに・をつけてね）", key="next_a")
buy_items = st.multiselect("ないもの・買ってほしいもの", ["・ウタマロ","・ハイター"], key="buy")
buy_add = st.text_area("追記（はじめに・をつけてね）", key="buy_a")

st.subheader("📝 共有事項")
names_input = st.text_area("来店された方のお名前", key="names_input", placeholder="カンマや改行で区切ってね")
cat1 = st.text_area("① 営業の様子", key="cat1_val")
cat2 = st.text_area("② 気づいたこと", key="cat2_val")
cat3 = st.text_area("③ その他", key="cat3_val")

st.divider()

# お名前のリスト化
name_list = [n.strip() for n in re.split(r'[,\n、。]', names_input) if n.strip()]
names_str = "\n".join(name_list) if name_list else "なし"

# 報告ボタン（横並び。スマホでは自動で縦になる）
btn_col1, btn_col2 = st.columns(2)

# 保存用データの共通辞書
report_data = {"done": done_items, "next": next_items, "buy": buy_items, "names": names_input, "cat1": cat1, "cat2": cat2, "cat3": cat3}

with btn_col1:
    if st.button("🕒 中間報告を保存", use_container_width=True):
        mid_txt = f"""

=========================
【中間報告】
=========================
前半でやったこと
{format_items(done_items, done_add)}

後半でやってほしいこと
{format_items(next_items, next_add)}

【連絡事項】
①営業の様子
{cat1 if cat1 else "特になし"}

②気づいたこと
{cat2 if cat2 else "特になし"}

{cat3 if cat3 else ""}

"""
        save_report(str(datetime.now().date()), "中間", mid_txt, report_data)
        st.code(mid_txt)
with btn_col2:
    if st.button("🚀 最終報告を保存", use_container_width=True):
        final_txt = f"""
====================================
**終業報告** 
====================================

【今日やったこと】
{format_items(done_items, done_add)}

【明日やってほしいこと】
{format_items(next_items, next_add)}

【買ってほしいもの】
{format_items(buy_items, buy_add)}

【来店人数】
新規　　　{val_new}名
リピ　　　{val_repeat}名
￣￣￣￣￣￣￣￣￣￣￣￣￣￣
計　　　　{all_customer}名

【来店者記録】
{names_str}

【連絡事項】
①営業の様子
{cat1 if cat1 else "特になし"}

②気づいたこと
{cat2 if cat2 else "特になし"}

{cat3 if cat3 else ""}

【レジ締め過不足】
¥45,000 
"""
        save_report(str(datetime.now().date()), "終業", final_txt, report_data)
        st.balloons()
        st.code(final_txt)
