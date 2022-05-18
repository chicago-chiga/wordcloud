import argparse
import os
from re import L
import sys
import traceback
from logging import config, getLogger

import yaml

from wordcloud_module import module_wordcloud as mw

"""
create word cloud
"""

if __name__ == '__main__':
    try:
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        # log
        log_config = os.path.join(cur_dir, 'logconf.yaml')
        config.dictConfig(
            yaml.load(open(log_config, encoding='utf8').read(), Loader=yaml.SafeLoader))
        logger = getLogger('logger')
        logger.info('===開始===')

        # load setting.yaml
        parser = argparse.ArgumentParser(add_help=True)
        parser.add_argument('-y', '--yaml', default='setting.yaml',
                            help='設定用のyamlファイル名')
        parser.add_argument(
            '-c', '--count', action='store_true', help='文字数カウント結果を表示')
        args = parser.parse_args()
        setting_yaml = os.path.join(cur_dir, args.yaml)

        with open(setting_yaml, 'r', encoding='utf8') as f:
            settings = yaml.safe_load(f)

        if settings['file_dir'] == None:
            file_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            file_dir = settings['file_dir']

        input_txt = os.path.join(file_dir, settings['input_txt'])
        user_dic = os.path.join(file_dir, settings['user_dic'])
        output_words_txt = os.path.join(file_dir, settings['output_words'])
        font_path = settings['font_path']
        wordcloud_png = os.path.join(file_dir, settings['wordcloud_png'])
        stop_words = settings['stop_words']
        top_rank = settings['top_rank']
    except Exception:
        t = traceback.format_exc()
        logger.error('===設定エラー===')
        logger.error(t)
        sys.exit(1)

    try:
        # call wordcloud_module
        mw.split_text(input_txt, output_words_txt, user_dic, stop_words)
        mw.put_wordcloud(output_words_txt, wordcloud_png, font_path)

        logger.info('===ファイル作成完了===')
        logger.info('---作成ファイル' + wordcloud_png + '"')

    except Exception:
        t = traceback.format_exc()
        logger.error('===ファイル作成エラー===')
        logger.error(t)
        sys.exit(1)

    try:
        # 文字カウント（オプション指定ありのとき）
        if args.count:
            logger.info('===文字数カウント開始===')
            mw.count_word(output_words_txt, top_rank)
            logger.info('===文字数カウント終了')
    except Exception:
        t = traceback.format_exc()
        logger.error('===文字数カウントエラー===')
        logger.error(t)
        sys.exit(1)
