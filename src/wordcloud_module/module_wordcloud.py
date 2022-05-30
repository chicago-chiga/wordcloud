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


def split_text(src, out, udic_file, stop_words, udic_type):
    try:
        a = word_extraction(udic_file, udic_type, stop_words)

        with open(src, encoding='utf8') as f1:
            with open(out, mode='w', encoding='utf8') as f2:
                for line in f1:
                    tokens = list(a.analyze(line))
                    f2.write('%s\n' % ' '.join(tokens))
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


def count_word(word_file, top_rank, user_dic, udic_type, count, put_file, count_file):
    try:
        if put_file:
            with open(count_file, mode='w', encoding='utf8') as f:
                words = wc(word_file, top_rank, user_dic, udic_type,
                           ['名詞', '動詞', '形容詞', '形容動詞', '感動詞'])
                for k, v in words:
                    f.write('%s\t%d\n' % (k, v))
                    if count:
                        print('%s:%d\n' % (k, v))
        else:
            words = wc(word_file, top_rank, user_dic, udic_type,
                       ['名詞', '動詞', '形容詞', '形容動詞', '感動詞'])
            for k, v in words:
                print('%s:%d\n' % (k, v))
    except:
        raise
