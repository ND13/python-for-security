# python-for-security
Some example of how a security analyst might use Python.

# Origin
I had a friend ask for examples of how security analysts use Python in their day to day work. The reality is that it varies widely because security is super broad. I'm just going to pick stuff I think analysts might encounter or should be able to do, just my opinion.

# Log parsing
Realistically, you probably won't have to do this by hand, at least I hope not, because your logs should already be nicely parsed out for you in a SIEM. But I actually think this is a good starting point and something good to do by hand because it will give you a better understanding about the structure of your logs and will allow you to better query them.


## Fake Log Types Overview
Under the /fake_logs/ directory there are 4 log files of differing types. Don't worry it's all fake logs that I generated via a Python script.

(log generator script not included :P)

((actually after looking at all of this and reading the code that is parsing the logs, go figure out how to use the `random` module to generate your own fake logs, timestamps and ip addresses are the randomly generated values)).

### 1. **Web Server Logs**
- **Format**: Apache-style combined logs
- **Fields**: IP address, timestamp, HTTP method, referer URL, user agent

---

### 2. **Authentication Logs**
- **Format**: Custom structured logs for login attempts
- **Fields**: Timestamp, status (e.g., FAILED, SUCCESS), username, IP address, port

---

### 3. **Windows Process Logs**
- **Format**: Pipe-separated (`|`) with labels
- **Fields**: Timestamp, parent process, child process, command line

---

### 4. **Firewall Logs**
- **Format**: Space-separated logs with port included in destination
- **Fields**: Timestamp, action (ALLOW/DENY), protocol, source IP, destination IP, destination port

## Log Parser Scripts Overview
Under the /log_parsers/ directory there are 4 python scripts that correspond to their respective log types. These scripts parse their respective log types breaking them into their key fields and writing them to a dictionary.

They all follow a similar format and probably should be put into a single "log_parser.py" script but I thought it would be easier on the eyes to keep it separated. 

The key thing here is just identifying within the actual logs themselves how they could potentially be split up. In other words, how are they already separated in the log itself, comma separated, spaces, pipes, etc.

It's all basic python string manipulation and using split(), if all else fails there's always a regex to get exactly what you need.

Let's look at some highlights. Here's an access log:

`2025-05-23 22:46:59 sshd[7222]: Failed password for test from 170.163.215.165 port 15037 ssh2` 

This one is pretty simple as everything can be broken up by spaces " ". A little bit of string manipulation is required to consolidate the timestamp `timestamp = split_logs[0] + ' ' + split_logs[1]` where we're just joining the two index positions that broke apart the timestamp, but it's really just .split(' ') taking care of everything else.

For the web server logs we used a little bit of string formatting to adjust the timestamp `formatted_timestamp = str(datetime.strptime(raw_timestamp, f"%d/%b/%Y:%H:%M:%S")) + ' ' + split_logs[4][:-1]`. 

Once we're done with splitting up and parsing the logs, we can assign them to python dictionaries to create key value pairs that we can access by name. 

An example of a parsed web log below:
`{'ip': '132.238.154.190', 'timestamp': '2025-05-23 21:57:59 -0700', 'method': 'POST /index.html HTTP/1.1', 'referer': 'http://malicious-login.biz', 'user_agent': 'Mozilla/5.0'}`

Now if I want to start analyzing fields I can just call them by name like user_agent, ip or referer. 

## Python Skills Required for Log Parsing Scripts
Pretty much any intro to Python video will cover everything needed to create scripts like this. "Skills" used in this:
- File I/O  
- String Manipulation  
- Lists and Dictionaries  
- For Loops  
- If Statements  
- Function Definition and Return  
- Date/Time Parsing
- Data Structuring 
- Basic Use of `shlex.split()` (for quoted strings)  

