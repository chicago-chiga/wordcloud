# WordCloud作成ツール
Janome(https://mocobeta.github.io/janome/) を使って、単語数カウント・WordCloudをするためのツール

## environment

1. Python  
over ver.3.7
1. library  

    ```text
    Janome==0.4.2
    PyYAML==6.0
    wordcloud=1.8.1
    streamlit==1.9.1
    ```

    * pip

    ```bash
    pip install wordcloud
    pip install PyYAML
    pip install janome
    pip install streamlit  # ブラウザの場合
    ```

## directory

```
|--.gitignore
|--README.md
|--error.log
|--file_dir  # バッチの場合
|  |--error.log            # エラー発生時のログ  
|  |--(分析対象のテキスト)
|  |--(単語分割ファイル)    # 自動で作成される
|  |--(ユーザー辞書)
|
|--src
|  |--st_create_wordcloud.py   # ブラウザ版 main
|  |--create_wordcloud.py      # バッチ版 main
|  |--create_wordcloud_all.py  # バッチ版(一括実行用) main
|  |--logconf.yaml             # ログ設定 バッチ用
|  |--setting.yaml             # 入出力ファイル、辞書などの設定 
|  |--wordcloud_module
|  |  |--module_wordcloud.py
|  |  |--stopword_filter.py
```

## 実行準備（バッチ版）

1. 入出力ファイルの設定
    `setting.yaml`に入出力フォルダ・ファイルを記載する

    setting.yaml(例)

    ```yaml
    # define folder and file

    # 入出力ファイルの置き場所（指定しない場合は現在のフォルダ。絶対パス）
    file_dir: /c/dev/wordcloud/file_dir

    # 分析対象の入力ファイル（必須）
    input_txt: review.txt

    # ユーザ辞書の名前（必須）
    user_dic: udic.csv

    # ユーザ辞書のタイプ（ipadic形式かsimpledic形式を選択）
    # udic_type: ipadic
    udic_type: simpledic

    # 一時ファイル名（固定でよい）
    output_words: tmp_words.txt

    # 出力するwordcloudファイルのフォントファイルのパス（TTFファイル）
    font_path: /c/dev/wordcloud/font/YuGothB003.ttf

    # 出力するwordcloud画像ファイル名（必須：拡張子はpng）
    wordcloud_png: wc_review.png

    # バッチ用(指定しない場合はfile_dir)
    # 分析対象の入力ファイル（バッチ用）
    input_dir: /c/wordcloud/in_batch_dir
    # 分析対象の出力ファイル（バッチ用）
    output_dir: /c/wordcloud/out_batch_dir

    # 除外する単語があれば指定する
    stop_words:
    - "ほしい"
    - "欲しい"
    - "する"
    - "れる"
    - "いる"
    - "-"
    # 文字数カウントオプションで上位何番目まで表示するか
    top_rank: 40
    ```

1. エラーログの出力先の設定
    * ログの設定は、`logconf.yaml`に記載されている
    * ログの出力先は、通常はコンソールのみに表示されるが、エラー時にはエラーログが
    `filename:`で指定したパスに出力される
    * エラーログは、エラー発生ごとに追記されるので、不要になれば削除しておくこと。（ファイルサイズが大きくなる）

    logconf.yaml（例）

    ```yaml
    h2:
    class: logging.FileHandler
    level: WARN
    formatter: fmt1
    filename: /c/dev/wordcloud/file_dir/error.log  # ←ここを書き換える
    encoding: utf8
    ```

1. ユーザー辞書の記入
    * 1.の`setting.yaml`の`user_dic`に指定したファイルに、以下のようなcsv形式で単語などを登録すると、単語としてカウントされる。
    * 例えば、「開始」と「時刻」ではなく「開始時刻」という1単語でカウントしたい場合や、一般の辞書にはない固有名詞などを記載しておく。

    * ユーザ辞書についてはjanome HPの「ユーザー定義辞書を使う」を参照（https://mocobeta.github.io/janome/#id8)

## 実行（バッチ版）
1ファイルを指定して分析する場合は、`create_wordloud.py` を実行
対象ディレクトリを指定して複数ファイルをまとめて分析する場合は、`create_wordloud_all.py` を実行する

* srcフォルダで実行

    ```bash
    # yaml指定なし（デフォルトはseting.yaml)
    python create_wordloud.py

    # yamlを指定
    python create_wordcloud.py --yaml(-y {設定を記載したyamlファイル})

    # 単語数カウントの結果をコンソールに表示
    python create_wordcloud.py --count(-c)

    # 単語数カウント結果をファイルに出力
    # 出力ファイルは、setting.yamlのwordcloud_pngファイルの拡張子を.txtにしたもの
    python create_wordcloud.py --write(-w)

    # 単語数をコンソールにもファイルにも出力する場合は、両方のオプションを指定する
    python create_wordcloud.py -c -w

    # ディレクトリにある複数ファイルをすべて分析する場合(単語数のカウントも実施)
    python create_wordcloud_all.py -c -w

    # help
    python create_wordcloud.py -h
    ```

## 実行（ブラウザ版）

* Streamlit版を起動

    ```bash
    # simple running
    streamlit run st_create_wordcloud.py

    # filter loopback address
    streamlit run --server.address localhost st_create_wordcloud.py
    ```

* 表示されたURL（デフォルトは  http://localhost:8501) をブラウザで起動する

* cf [documentation](https://docs.streamlit.io/)
