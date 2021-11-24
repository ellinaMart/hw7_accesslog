import os
import sys
import json
import re
import argparse
from collections import defaultdict, Counter


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


parser = argparse.ArgumentParser(description='Process access.log')
parser.add_argument('-f', dest='file', action='store', help='Path to log file')
#parser.add_argument('--path', type=dir_path)
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
dict_method = defaultdict(
    lambda: {"GET": 0, "POST": 0, "PUT": 0, "DELETE" : 0, "HEAD": 0}
)
dict_ip = defaultdict(
    lambda: {"GET": 0, "POST": 0, "PUT": 0, "DELETE" : 0, "HEAD": 0}
)
ips = []

with open(args.file) as file:
    idx = 0
    for line in file:
        # if idx > 99:
        #     break

#109.169.248.247 - - [12/Dec/2015:18:25:11 +0100] "GET /administrator/ HTTP/1.1" 200 4263 "-" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" 7269
        ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",line)
        if ip_match is not None:
            ip = ip_match.group()
            ips.append(ip)
            #dict_ip[0]["ip"] = ip
            #dict_ip[0]["count"] += 1
        method = re.search(r"\] \"(POST|GET|PUT|DELETE|HEAD)",line)
        if method is not None:
            dict_ip[ip][method.groups()[0]] += 1
            #idx += 1
            if method.groups()[0] == "GET":
                #import pdb; pdb.set_trace()
                dict_method[0]['GET'] += 1
            elif method.groups()[0] == "POST":
                dict_method[0]['POST'] += 1
            elif method.groups()[0] == "PUT":
                dict_method[0]['PUT'] += 1
            elif method.groups()[0] == "DELETE":
                dict_method[0]['DELETE'] += 1
            elif method.groups()[0] == "HEAD":
                dict_method[0]['HEAD'] += 1

SUM = dict_method[0]['GET'] + dict_method[0]['POST'] + dict_method[0]['PUT'] + dict_method[0]['DELETE'] + dict_method[0]['HEAD']
cnt_ip = Counter()

#print(json.dumps(dict_ip,indent=4))
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(dict_ip, f, ensure_ascii=False, indent=4)

print(json.dumps(dict_method, indent=4))
print('SUM of requests:', SUM)
print("Most popular ips are:", Counter(ips).most_common(3))
#import pdb;pdb.set_trace()








