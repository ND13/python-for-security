# web log parser

import shlex
from datetime import datetime


def log_parser(log_file):

    parsed_logs = []
    
    with open(f'{log_file}', 'r') as logs:
        
        for line in logs:
            split_logs = shlex.split(line)

            ip_address = split_logs[0]
            raw_timestamp = split_logs[3][1:]
            formatted_timestamp = str(datetime.strptime(raw_timestamp, f"%d/%b/%Y:%H:%M:%S")) + ' ' + split_logs[4][:-1]

            http_method = split_logs[5]
            referer_url = split_logs[8]
            user_agent = split_logs[9]

            print(ip_address, formatted_timestamp, http_method, referer_url, user_agent)

            parsed_logs.append({
                'ip': ip_address,
                'timestamp': formatted_timestamp,
                'method': http_method,
                'referer': referer_url,
                'user_agent': user_agent
            })

    if parsed_logs:
        print(parsed_logs)
        return parsed_logs
    else:
        return False

print(log_parser('..\\fake_logs\\web_access.log'))
