__author__ = 'manasvi'
import yaml
from activity import Activity
import os
a = yaml.load_all(file("config.yaml"))
for doc in a:
    print(doc)



def parse(config_file_path):
    activity_list = []
    for doc in yaml.load_all(config_file_path):
        activity_list.append(
            Activity()
        )