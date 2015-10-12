__author__ = 'manasvi'
import os
# A set of tasks to be run in a specific order. The order is specified by the list.


class Activity:

    def __init__(self, test_folder_path, src_file_extension=".c", output_folder_path=None, output_file_extension=None,
                 result_file_path=None, result_file_extension=None):
        self.test_folder_path = os.path.abspath(test_folder_path)
        self.src_file_extension = src_file_extension
        if output_folder_path is None:
            self.output_folder_path = os.path.join(test_folder_path, os.path.basename(test_folder_path) + ".pykrunner")
        else:
            self.output_folder_path = os.path.abspath(output_folder_path)

        if output_file_extension is None:
            self.output_file_extension = ".out"

        else:
            self.output_file_extension = output_file_extension

        if result_file_path is None:
            self.result_file_path = os.path.join(test_folder_path, os.path.basename(test_folder_path) + ".pykresult")

        else:
            self.result_file_path = os.path.abspath(result_file_path)

        if result_file_extension is None:
            self.result_file_extension = ".pyk"

        else:
            self.result_file_extension = result_file_extension
    






