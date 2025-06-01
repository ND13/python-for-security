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


---


## IOC Checking Script (ioc_checker.py) ##
Cool we parsed some logs and spit them into a dictionary but what can we do with them?

Let's pretend we got some IOCs from some OSINT platform. Maybe we pulled it through an API (hmm, maybe we'll look at doing that next) or it got sent to us via some report/email.
`"http://malicious-login.biz", "http://evil-phishing.com"` 

Here are two domains which are associated with some kind of malicious activity. Lets say phishing attempts for credential harvesting. 

Well now that our logs are parsed, we can go through them and see if we have any hits for these domains in our logging that might indicate if we're being used as part of some phishing campaign.

For simplicity and the visual I've pasted all the parsed logs into a 'logs' variable in the ioc_checker.py script.

What's nice about the parsing is we can access each log's referer value and check for the malicious domains.

`for log in logs:
    if log['referer'] in malicious_domains:
        malicious_domain_count_dict[log['referer']] = malicious_domain_count_dict.get(log['referer'], 0) + 1 
        print(f"Malicious domain: {log['referer']} observed in logs. Full log below\n ==={log}===:")`

This simple loop lets us look at each log in the logs list, then access the referer key in each log and compare it to the list of malicious domains. If the 'referer' field matches any of the domains in the malicious_domains list, we'll add it to a separate dictionary to get count of how many times that domain appeared; and we'll also print out the domain that was found and it's associated log.

An example of our output.
`Malicious domain: http://malicious-login.biz observed in logs. Full log below
 ==={'ip': '76.113.252.93', 'timestamp': '2025-05-23 22:45:59 -0700', 'method': 'POST /index.html HTTP/1.1', 'referer': 'http://malicious-login.biz', 'user_agent': 'Mozilla/5.0'}===:`

What might this indicate to us? Well, if we're seeing these malicious domains in our referer field of our Apache logs that could mean users are being redirected to our legitimate website from phishing domains.

Imagine you're a phisher looking for credentials and you create a fake login page imitating a legitimate website. You get someone to submit credentials to your phishing site and then you redirect them to the legitimate site after they submit to yours and have been successfully tricked into giving up their creds.

It might be your customers accounts getting popped or your employees getting popped, so best to identify these things when you can and get the phishing sites reported/taken down. This is just one example of malicious domains appearing in your referer field of web server logs, they can be indicators of other sneaky activity too.

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



