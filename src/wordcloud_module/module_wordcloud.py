import matplotlib.pyplot as plt
from janome.analyzer import Analyzer
from janome.charfilter import RegexReplaceCharFilter
from janome.tokenfilter import (ExtractAttributeFilter, POSKeepFilter,
                                POSStopFilter, TokenCountFilter)
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud

from wordcloud_module.stopword_filter import StopWordFilter


class MyTokenezer:

    def __init__(self):
        pass

    def set_tokenizer(self, user_dic, udic_type):
        my_tokenizer = Tokenizer(
            user_dic, udic_enc='utf8', udic_type=udic_type) if user_dic else Tokenizer()
        return my_tokenizer


class MyTokenFilter:

    def __init__(self):
        # 必要な品詞だけにしぼる
        self.pos_keeplist = ['名詞', '動詞', '形容詞', '形容動詞', '感動詞']
        self.pos_stoplist = ['名詞,非自立', '名詞,代名詞']
        self.extract_attribute_filter = 'base_form'

    def set_token_filter4split(self, stop_word):
        my_token_filters = [POSKeepFilter(self.pos_keeplist),
                            POSStopFilter(self.pos_stoplist),
                            StopWordFilter(word_list=stop_word),
                            ExtractAttributeFilter(
                                self.extract_attribute_filter)
                            ]
        return my_token_filters

    def set_token_filter4count(self):
        my_token_filters = [POSKeepFilter(self.pos_keeplist),
                            TokenCountFilter(sorted=True, att='base_form')]
        return my_token_filters


class MyAnalyzer:
    def __init__(self):
        pass

    def set_analyzer4split(self, char_filters, tokenizer, token_filters):
        my_analyzer = Analyzer(char_filters=char_filters, tokenizer=tokenizer,
                               token_filters=token_filters)
        return my_analyzer

    def set_analyzer4count(self, tokenizer, token_filters):
        my_analyzer = Analyzer(tokenizer=tokenizer,
                               token_filters=token_filters)
        return my_analyzer


# テキスト分割


def split_text(src, user_dic, stop_words, udic_type):
    try:
        char_filters = [RegexReplaceCharFilter('《．＊？》', '')]
        tokenizer = MyTokenezer().set_tokenizer(user_dic, udic_type=udic_type)
        token_filters = MyTokenFilter().set_token_filter4split(stop_words)

        a = MyAnalyzer().set_analyzer4split(char_filters, tokenizer, token_filters)

        token_list = []
        with open(src, encoding='utf8') as f1:
            for line in f1:
                tokens = list(a.analyze(line))
                token_list.append(tokens)
            return token_list
    except:
        raise

# 単語数カウント


def count_word(word_file, top_rank, user_dic,  udic_type):
    try:
        tokenizer = MyTokenezer().set_tokenizer(user_dic, udic_type=udic_type)
        with open(word_file, 'r', encoding='utf8') as f:
            token_filters = MyTokenFilter().set_token_filter4count()

            a = MyAnalyzer().set_analyzer4count(tokenizer, token_filters)
            text = f.read()
            return list(a.analyze(text))[:top_rank]
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

# WordCloudファイル作成


def put_wordcloud(word_file, png_file, font_path):
    try:
        with open(word_file, encoding='utf8') as f:
            text = f.read()
            wordcloud = WordCloud(font_path=font_path,
                                  background_color='white',
                                  width=1024, height=674).generate(text)
            wordcloud.to_file(png_file)
            return True
    except:
        raise
