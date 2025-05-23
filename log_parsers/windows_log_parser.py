
def log_parser(log_file):
    
    parsed_logs = []

    with open(log_file, 'r') as logs:
        for line in logs:
            split_logs = line.split('|')
            stripped_log = [s.strip() for s in split_logs]
            print(stripped_log)

            timestamp = stripped_log[0]
            parent = stripped_log[1].split(": ", 1)[1]
            child = stripped_log[2].split(": ", 1)[1]
            command_line = stripped_log[3].split(": ", 1)[1]

            parsed_logs.append({
                'timestamp': timestamp,
                'parent': parent,
                'child': child,
                'command_line': command_line
            })
        
        if parsed_logs:
            return parsed_logs
        else:
            print('no logs')
            return False

print(log_parser('..\\fake_logs\\windows_process.log'))
