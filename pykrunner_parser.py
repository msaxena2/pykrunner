__author__ = 'manasvi'
import yaml
from activity import Activity
import exceptions

def parse(config_file_path):
    activity_list = []
    try:
        for doc in yaml.load_all(open(config_file_path)):
            activity_list.append(
                Activity(doc["test_folder_path"], doc.get("test_file_extension"), doc.get("output_folder_path"),
                         doc.get("output_file_extension"), doc.get("result_folder_path"), doc.get("result_file_extension"),
                         doc.get("thread_count")
                ))
        return activity_list
    except exceptions.OSError as oserror:
        print oserror.strerror

