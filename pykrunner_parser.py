__author__ = 'manasvi'
import yaml

a = yaml.load_all(file("config.yaml"))
for doc in a:
    print(doc)
