import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile

# --- ページ設定 & デザイン ---
st.set_page_config(page_title="和風ファイル変換器", layout="centered")

# カスタムCSSで雰囲気を少し黒・赤基調に
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; color: #ffffff; }
    .stButton>button { background-color: #b03a2e; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎴 拡張子一括変換ツール")
st.write("アップロードしたファイルの拡張子を書き換えて、ZIPでまとめてダウンロードできます。")

# --- 設定エリア ---
col1, col2 = st.columns(2)
with col1:
    from_suffix = st.text_input("変換前の拡張子", value=".txt")
with col2:
    to_suffix = st.text_input("変換後の拡張子", value=".md")

# --- ファイルアップロード ---
uploaded_files = st.file_uploader(
    "ファイルを選択してください（複数可）", 
    accept_multiple_files=True
)

if uploaded_files:
    # 変換後のファイルを一時的に保存するメモリ
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        success_count = 0
        
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            
            # 拡張子の判定と置換
            if file_name.endswith(from_suffix):
                # 新しい名前の作成
                base_name = file_name.rsplit(from_suffix, 1)[0]
                new_name = base_name + to_suffix
                
                # ZIPの中にリネームして追加
                zip_file.writestr(new_name, uploaded_file.getvalue())
                success_count += 1
                st.success(f"変換準備完了: {file_name} -> {new_name}")
            else:
                st.warning(f"スキップ（対象外）: {file_name}")

    # --- ダウンロードボタン ---
    if success_count > 0:
        st.divider()
        st.download_button(
            label="🏮 変換したファイルをダウンロード (ZIP)",
            data=zip_buffer.getvalue(),
            file_name="converted_files.zip",
            mime="application/zip"
        )
    else:
        st.info("対象の拡張子を持つファイルがありません。")
