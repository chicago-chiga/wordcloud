import matplotlib.pyplot as plt
from janome.analyzer import Analyzer
from janome.charfilter import RegexReplaceCharFilter
from janome.tokenfilter import (ExtractAttributeFilter, POSKeepFilter,
                                POSStopFilter, TokenCountFilter)
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud

from wordcloud_module.stopword_filter import StopWordFilter


def word_extraction(udic_file, udic_type, stop_words):
    try:
        tokenizer = Tokenizer(udic_file, udic_enc='utf8',
                              udic_type=udic_type) if udic_file else Tokenizer()
        char_filters = [RegexReplaceCharFilter('《．＊？》', '')]

        # 必要な品詞だけにしぼる
        token_filters = [POSKeepFilter(['名詞', '動詞', '形容詞', '形容動詞', '感動詞']),
                         POSStopFilter(['名詞,非自立', '名詞,代名詞']),
                         StopWordFilter(word_list=stop_words),
                         ExtractAttributeFilter('base_form')]
        return Analyzer(char_filters=char_filters, tokenizer=tokenizer,
                        token_filters=token_filters)
    except:
        raise


def show_wordcloud(word_file, font_path):
    try:
        with open(word_file, encoding='utf8') as f:
            text = f.read()
            wordcloud = WordCloud(font_path=font_path,
                                  background_color='white',
                                  width=1024, height='674').generate(text)
            plt.imshow(wordcloud, interpolation='billnear')
            plt.axis('off')
            plt.figure()
            plt.show()
    except:
        raise


def put_wordcloud(word_file, png_file, font_path):
    try:
        with open(word_file, encoding='utf8') as f:
            text = f.read()
            wordcloud = WordCloud(font_path=font_path,
                                  background_color='white',
                                  width=1024, height=674).generate(text)
            wordcloud.to_file(png_file)
    except:
        raise


def wc(file, top_rank, user_dic, udic_type, pos=[]):
    try:
        tokenizer = Tokenizer(
            user_dic, udic_enc='utf8', udic_type=udic_type) if user_dic else Tokenizer()
        with open(file, 'r', encoding='utf8') as f:
            if not pos:
                token_filters = [TokenCountFilter(
                    sorted=True, att='base_form')]
            else:
                token_filters = [POSKeepFilter(pos), TokenCountFilter(
                    sorted=True, att='base_form')]
            a = Analyzer(tokenizer=tokenizer, token_filters=token_filters)
            text = f.read()
            return list(a.analyze(text))[:top_rank]
    except:
        raise

# 単語数カウント


def count_word(word_file, top_rank, user_dic,  udic_type):
    try:
        count_result = wc(word_file, top_rank, user_dic, udic_type,
                          ['名詞', '動詞', '形容詞', '形容動詞', '感動詞'])
        return count_result
    except:
        raise

# 単語分割


def split_text(src, udic_file, stop_words, udic_type):
    try:
        a = word_extraction(udic_file, udic_type, stop_words)
        token_list = []
        with open(src, encoding='utf8') as f1:
            for line in f1:
                tokens = list(a.analyze(line))
                token_list.append(tokens)
            return token_list
    except:
        raise
