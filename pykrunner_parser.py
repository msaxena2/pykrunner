__author__ = 'manasvi'
import yaml
from activity import Activity


def parse(config_file_path):
    activity_list = []
    try:
        for doc in yaml.load_all(open(config_file_path)):
            activity_list.append(
                Activity(doc["test_folder_path"], doc.get("test_file_extension"), doc.get("output_folder_path"),
                         doc.get("output_file_extension"), doc.get("result_file_path"), doc.get("result_file_extension")
                ))
            return activity_list
    except Exception:
        print "Config File " + config_file_path + " couldn't be parsed"

