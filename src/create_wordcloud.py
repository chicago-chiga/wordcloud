import argparse
import csv
import os
import sys
import traceback
from logging import config, getLogger
from pathlib import Path

import yaml

from wordcloud_module import module_wordcloud as mw
from wordcloud_module import yaml_settings


def set_args():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-y', '--yaml', default='setting.yaml',
                        help='設定用のyamlファイル名')
    parser.add_argument(
        '-c', '--count', action='store_true', help='文字数カウント結果を表示')
    parser.add_argument(
        '-w', '--write', action='store_true', help='文字数カウントファイルを出力')
    args = parser.parse_args()
    return args


def main():
    try:
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        # log
        log_config = os.path.join(cur_dir, 'logconf.yaml')
        config.dictConfig(
            yaml.load(open(log_config, encoding='utf8').read(), Loader=yaml.SafeLoader))
        logger = getLogger('logger')
        logger.info('===開始===')

        # オプション引数
        args = set_args()

        # setting
        setting_yaml = os.path.join(cur_dir, args.yaml)

        with open(setting_yaml, 'r', encoding='utf8') as f:
            yaml_file = yaml.safe_load(f)
            setting = yaml_settings.Settings_Single(yaml_file)

    except Exception:
        t = traceback.format_exc()
        logger.error('===設定エラー===')
        logger.error(t)
        sys.exit(1)

    try:
        # 単語分割
        word_list = mw.split_text(
            setting.input_txt, setting.user_dic, setting.stop_words, setting.udic_type)
        with open(setting.output_words_txt, mode='w', encoding='utf8') as f2:
            writer = csv.writer(f2, delimiter=' ')
            writer.writerows(word_list)

        if args.count or args.write:
            logger.info('===単語数カウント開始===')
            # 単語数カウント
            word_count = mw.count_word(
                setting.output_words_txt, setting.top_rank, setting.user_dic, setting.udic_type)

            # 標準出力
            if args.count:
                for k, v in word_count:
                    print('%s\t%d' % (k, v))

            # ファイル出力
            if args.write:
                count_file = os.path.join(setting.file_dir, Path(
                    setting.wordcloud_png).stem + '.txt')
                logger.info(f"---カウント結果ファイル: {count_file} ")
                with open(count_file, mode='w', encoding='utf8') as f3:
                    for k, v in word_count:
                        f3.write('%s\t%d\n' % (k, v))
            else:
                count_file = None
            logger.info('===単語数カウント終了===')

    except FileNotFoundError:
        t = traceback.format_exc()
        logger.error('===ファイル指定エラー===')
        logger.error(t)
        sys.exit(1)

    except Exception:
        t = traceback.format_exc()
        logger.error('===単語数カウントエラー===')
        logger.error(t)
        sys.exit(1)

    try:
        # word cloud 作成
        result = mw.put_wordcloud(setting.output_words_txt,
                                  setting.wordcloud_png, setting.font_path)
        if result:
            logger.info('---WordCloudファイル' + setting.wordcloud_png + '"')
            logger.info('===ファイル作成完了===')
    except Exception:
        t = traceback.format_exc()
        logger.error('===WordCloudファイル作成エラー===')
        logger.error(t)
        sys.exit(1)


# 1ファイルのみの場合
if __name__ == '__main__':
    main()
