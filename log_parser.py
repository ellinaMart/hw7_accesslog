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
durations = []

with open(args.file) as file:
    for line in file:
        ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",line)
        duration_match = line.rsplit(None, 1)[-1]
        durations.append(duration_match)
        if ip_match is not None:
            ip = ip_match.group()
            ips.append(ip)
            #dict_ip[0]["ip"] = ip
            #dict_ip[0]["count"] += 1
        method = re.search(r"\] \"(POST|GET|PUT|DELETE|HEAD)",line)
        if method is not None:
            dict_ip[ip][method.groups()[0]] += 1
            if method.groups()[0] == "GET":
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
durations.sort()
print ('3 most long requests:', durations[-1], durations[-2], durations[-3])
top_durations_data = [{'method': '', 'url': '', 'ip': '', 'duration': ''},
                      {'method': '', 'url': '', 'ip': '', 'duration': ''},
                      {'method': '', 'url': '', 'ip': '', 'duration': ''}]
with open(args.file) as file:
    for line in file:
        top_durations = [durations[-1], durations[-2], durations[-3]]
        duration_match = line.rsplit(None, 1)[-1]
        i=0
        if duration_match in top_durations:
            while i < 3:
                ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
                method = re.search(r"\] \"(POST|GET|PUT|DELETE|HEAD)", line)
                url = re.search(r'(https?://[\S]+)', line)
                top_durations_data[i]['method'] = method.groups()
                top_durations_data[i]['ip'] = ip_match.group()
                top_durations_data[i]['duration'] = duration_match
                if url is not None:
                    top_durations_data[i]['url'] = url.groups()
                i=i+1

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(dict_ip, f, ensure_ascii=False, indent=4)
    json.dump({'Sum of requests': SUM}, f, ensure_ascii=False, indent=4)
    json.dump({'Most popular ips are:':Counter(ips).most_common(3)}, f, ensure_ascii=False, indent=4)
    json.dump({'Most long reqests:':top_durations_data}, f, ensure_ascii=False, indent=4)

print(json.dumps(dict_method, indent=4))
print('SUM of requests:', SUM)
print("Most popular ips are:", Counter(ips).most_common(3))
print("Most long reqests:", top_durations_data)

