__author__ = 'manasvi'


class Task:
    def __init__(self, executable, test_folder, source_file_extension, result_folder=None, result_file_extension=None):
        self.executable = executable
        self.test_folder = test_folder
        self.source_file_extension = source_file_extension
        self.result_folder = result_folder
        self.result_file_extension = result_file_extension
