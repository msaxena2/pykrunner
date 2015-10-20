__author__ = 'manasvi'
import os
# A set of tasks to be run in a specific order. The order is specified by the list.


class Activity:

    def __init__(self, test_folder_path, src_file_extension=".c", output_folder_path=None, output_file_extension=None,
                 result_folder_path=None, result_file_extension=None, thread_count=4):

        self.test_folder_path = os.path.abspath(os.path.normpath(test_folder_path))
        self.src_file_extension = src_file_extension
        if output_folder_path is None:
            # self.output_folder_path = os.path.join(test_folder_path, os.path.basename(test_folder_path) + "pykrunner")
            self.output_folder_path = test_folder_path
        else:
            self.output_folder_path = output_folder_path

        if output_file_extension is None:
            self.output_file_extension = ".out"

        else:
            self.output_file_extension = output_file_extension

        if result_folder_path is None:
            # self.result_folder_path = os.path.join(test_folder_path, os.path.basename(test_folder_path) + ".pykresult")
            self.result_folder_path = test_folder_path
        else:
            self.result_folder_path = result_folder_path

        if result_file_extension is None:
            self.result_file_extension = ".pyk"

        else:
            self.result_file_extension = result_file_extension

        if thread_count != 4:
            self.thread_count = thread_count

        else:
            self.thread_count = thread_count

        if not os.path.exists(result_folder_path):
            for path in os.path.split(os.path.abspath(result_folder_path)):
                if not os.path.exists(path):
                    os.mkdir(path)

        if not os.path.exists(output_folder_path):
            for path in os.path.split(os.path.abspath(output_folder_path)):
                if not os.path.exists(path):
                    os.mkdir(path)

