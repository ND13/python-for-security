
def log_parser(log_file):
    
    parsed_logs = []

    with open(log_file, 'r') as logs:
        for line in logs:
            split_logs = line.split(' ')
            stripped_logs = [s.strip() for s in split_logs]

            timestamp = stripped_logs[0] + ' ' + stripped_logs[1]
            action = stripped_logs[2]
            protocol = stripped_logs[3]
            src_ip = stripped_logs[5]
            dst_ip = stripped_logs[7]
            dst_port = dst_ip.split(':', 1)[1]

            parsed_logs.append({
                'timestamp': timestamp,
                'action': action,
                'protocol': protocol,
                'source_ip': src_ip,
                'destination_ip': dst_ip,
                'destination_port': dst_port
            })
        
        if parsed_logs:
            return parsed_logs
        else:
            print('no logs')
            return False

print(log_parser('..\\fake_logs\\firewall_connections.log'))
