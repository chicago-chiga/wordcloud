from janome.tokenfilter import TokenFilter


class StopWordFilter(TokenFilter):
    def __init__(self, word_list=[], word_list_file=''):
        self.word_list = []
        if word_list:
            self.word_list = word_list
        elif word_list_file:
            with open(word_list_file) as f:
                for line in f:
                    word = line.strip()
                    self.word_list.append(word)

    def apply(self, tokens):
        for token in tokens:
            if any(token.base_form == word for word in self.word_list):
                continue
            yield token
