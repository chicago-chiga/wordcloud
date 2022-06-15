import csv
import os
import tempfile
import time
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image

from wordcloud_module import module_wordcloud as mw


@st.cache(suppress_st_warning=True)
def create_temp_dir():
    dname = tempfile.TemporaryDirectory(prefix='stlit')
    return dname


def keep_count_result(count_result):
    st.session_state['count_result'] = count_result


def keep_wc_result(wc):
    st.session_state['wc'] = wc


def main():
    st.set_page_config(layout="wide")
    st.sidebar.header('テキスト分析ツール')
    st.sidebar.text('welcome!')

    # 一時ディレクトリ作成
    dname = create_temp_dir()

    # セッション初期化
    if 'count_result' not in st.session_state:
        st.session_state['count_result'] = None

    if 'wc' not in st.session_state:
        st.session_state['wc'] = None

    count_result = pd.DataFrame(index=[], columns=[])
    wc = None

    # サイドバーエリア
    st.sidebar.markdown('### 各種設定')

    # font_file
    st.sidebar.markdown('**フォントファイル [必須]**')
    font_file = st.sidebar.file_uploader(label='TTF形式のみ:')

    if font_file is not None:
        with open(os.path.join(dname.name, font_file.name), "wb") as tmp_font_file:
            font_path = Path(tmp_font_file.name)
            font_path.write_bytes(font_file.getvalue())

    # ユーザー辞書
    st.sidebar.markdown('**ユーザー辞書**')
    user_dic = st.sidebar.file_uploader(label='単語登録が必要なときだけ:')

    if user_dic is not None:
        # XXX: 信頼できないファイルは安易に評価しないこと

        with open(os.path.join(dname.name, user_dic.name), "wb") as tmp_user_dic:
            udic_path = Path(tmp_user_dic.name)
            udic_path.write_bytes(user_dic.getvalue())

    # udic_type
    st.sidebar.markdown('**辞書タイプ**')
    udic_type = st.sidebar.selectbox(
        'simpledic: 簡易版, ipadic: IPA形式',
        ("simpledic", "ipadic"))

    st.sidebar.write('You selected: ', udic_type)

    # stop word
    st.sidebar.markdown('**除去する単語**')
    stop_words = st.sidebar.text_area(
        label='分析対象から除去する単語を入力してください。　各単語は改行で区切ってください:').splitlines()
    st.sidebar.write('stop_words: ', stop_words)

    # rank
    st.sidebar.markdown('**単語カウント結果表示ランク**')
    top_rank = st.sidebar.number_input(label='単語カウント結果表示のときのみ', min_value=1)
    st.sidebar.write('top_rank: ', top_rank)

    # コンテンツエリア
    # input file
    st.markdown('**分析対象ファイル [必須]**')
    input_txt_file = st.file_uploader(label='utf-8形式:')

    if input_txt_file is not None:
        # XXX: 信頼できないファイルは安易に評価しないこと
        with open(os.path.join(dname.name, input_txt_file.name), "wb") as tmp_input:
            input_path = Path(tmp_input.name)
            input_path.write_bytes(input_txt_file.getvalue())

    # output file
    st.markdown('**WordCloudのダウンロードファイル名 [必須]**')
    wc_file = st.text_input(label='拡張子は「.png」を指定してください:')

    # wordcloud
    wc_file_path = os.path.join(dname.name, wc_file)

    # 単語カウント結果ファイル
    count_file_name = (os.path.splitext(
        os.path.basename(wc_file_path))[0]+'.txt')

    # ボタン活性化制御
    if font_file is None or input_txt_file is None or not wc_file:
        disable_flg = True
    else:
        disable_flg = False

    # 文字数カウント結果表示
    count_flg = st.checkbox('単語カウント結果も出力', disabled=disable_flg)

    # 分析処理
    start = st.button("分析開始！", disabled=disable_flg)

    if start:
        # Sessionクリア
        if 'count_result' in st.session_state.keys():
            del st.session_state['count_result']
        if 'wc' in st.session_state.keys():
            del st.session_state['wc']

        if user_dic is None:
            tmp_user_dic_name = ""
        else:
            tmp_user_dic_name = tmp_user_dic.name

        # 単語分割
        split_text = mw.split_text(
            tmp_input.name, tmp_user_dic_name, stop_words, udic_type)

        with open(os.path.join(dname.name, 'split_word.txt'), "w",  encoding='utf-8') as tmp_split_word:
            writer = csv.writer(tmp_split_word, delimiter=' ')
            writer.writerows(split_text)

        # progress bar
        text = st.empty()
        bar = st.progress(0)

        for i in range(100):
            text.text(f"分析中... {i + 1}/100")
            bar.progress(i + 1)
            time.sleep(0.01)

        # WordCloud作成
        wc = mw.put_wordcloud(
            tmp_split_word.name, wc_file_path, tmp_font_file.name)
        keep_wc_result(wc)

        # 単語カウント結果作成
        if count_flg:
            count_word = mw.count_word(tmp_split_word.name,
                                       top_rank, tmp_user_dic_name, udic_type)
            count_result = pd.DataFrame(
                count_word, columns=["単語  ", "出現数      "])
            keep_count_result(count_result)

    # 結果表示エリア
    if st.session_state.count_result is not None:
        with st.expander("単語カウント結果"):
            # sessionの結果を引き継ぐ
            session_result = st.session_state.count_result
            st.dataframe(session_result)

            count_file = session_result.to_csv(
                sep='\t', index=True).encode('utf8')

            dl_count_btn = st.download_button(
                label="Download",
                data=count_file,
                file_name=count_file_name,
                on_click=keep_count_result(session_result),
                mime='text/csv')

    if st.session_state.wc is not None:
        wc_img = Image.open(wc_file_path)
        st.image(wc_img)

        # wc_imgをセッションに入れる
        with open(wc_file_path, "rb") as img_file:
            dl_wc_btn = st.download_button(
                label="Download image",
                data=img_file,
                file_name=wc_file,
                on_click=keep_wc_result(wc_img),
                mime="image/png"
            )


if __name__ == '__main__':
    main()
