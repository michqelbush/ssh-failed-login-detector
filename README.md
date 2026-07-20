# ssh-failed-login-detector
 
Detects brute force SSH login attempts by parsing auth logs and flagging the suspicious IPs
 
I built this to try shaking off the rust after not using python for a good amount of time. I wanted to build something that would actually improve and help me work towards a real job in Cyber Security. Basically if an IP is repeatedly trying and failing to log in, it's the first sign of a brute force attack so instead of manually looking through the logs, the code catches it for you. I saw it recommended as a good first security project, so I built it.
 
## Use
 
    sudo python3 ssh_log_analyzer.py
 
The code defaults to /var/log/auth.log and flags anyone that has 3+ failed tries.
 
To point it at a different file or change the threshold is just:
 
    sudo python3 ssh_log_analyzer.py /path/to/log --threshold 5
 
## Example outputs

    Failed Login Summary
    185.220.101.45: 7 failed attempts SUS
    ::1: 3 failed attempts SUS
 
## How it works
A regex grabs the timestamp, username, and IP from each line with failed-password, and a tracker keeps track of how many times each IP shows up. If any IP goes over the set threshold they get flagged as SUS (Suspicious).
 
## Update: added automatic blocking
 
Flagging an IP is one thing, but it doesn't actually stop anything, so I added a `--block` flag that hooks into iptables and actually blocks the IP once it crosses the threshold.
 
    sudo python3 ssh_log_analyzer.py --block
 
It's off by default, so nothing gets blocked unless you ask for it. When it does block something, it prints the IP it's blocking before it does it, so it's not doing anything silently.
 
    Failed Login Summary
    203.0.113.99: 3 failed attempts SUS
    Blocking 203.0.113.99 via iptables
 
I think it was a good add because just showing the failed attempts doesnt actually do anything. Flagging and telling is good, but it should actually be able to do something about it.
 
## Next steps
 
Might add a mode that watches the log live instead of just reading it once. Also thinking about flagging it harder if a successful login follows a string of failures, which is worse than failures.
