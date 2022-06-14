import os


class SettingsClass:
    yaml_file = None
    file_dir = None
    user_dic = None
    udic_type = None
    font_path = None
    stop_words = None
    top_rank = None

    def __init__(self, yaml_file):
        self.yaml_file = yaml_file
        if yaml_file['file_dir'] == None:
            self.file_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.file_dir = yaml_file['file_dir']
        self.user_dic = os.path.join(self.file_dir, yaml_file['user_dic'])
        self.udic_type = yaml_file['udic_type']
        self.font_path = yaml_file['font_path']
        self.stop_words = yaml_file['stop_words']
        self.top_rank = yaml_file['top_rank']


class Settings_Single(SettingsClass):
    input_txt = None
    output_words_txt = None
    wordcloud_png = None

    def __init__(self, yaml_file):
        super().__init__(yaml_file)
        self.input_txt = os.path.join(self.file_dir, yaml_file['input_txt'])
        self.output_words_txt = os.path.join(
            self.file_dir, yaml_file['output_words'])
        self.wordcloud_png = os.path.join(
            self.file_dir, yaml_file['wordcloud_png'])


class Settings_Batch(SettingsClass):
    input_dir = None
    output_dir = None
    output_words_txt = None

    def __init__(self, yaml_file):
        super().__init__(yaml_file)

        if self.yaml_file['input_dir'] == None:
            self.input_dir = self.file_dir
        else:
            self.input_dir = self.yaml_file['input_dir']

        if self.yaml_file['output_dir'] == None:
            self.output_dir = self.file_dir
        else:
            self.output_dir = self.yaml_file['output_dir']
        self.output_words_txt = os.path.join(
            self.output_dir, yaml_file['output_words'])
