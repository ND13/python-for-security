
def log_parser(log_file):
    
    parsed_logs = []

    with open(log_file, 'r') as logs:
        for line in logs:
            split_logs = line.split(' ')

            timestamp = split_logs[0] + ' ' + split_logs[1]
            status = split_logs[3]
            user = split_logs[6]
            ip_address = split_logs[8]
            port = split_logs[10]

            parsed_logs.append({
                'timestamp': timestamp,
                'status': status,
                'user': user,
                'ip': ip_address,
                'port': port
            })
        
        if parsed_logs:
            return parsed_logs
        else:
            print('no logs')
            return False

print(log_parser('..\\fake_logs\\auth.log'))