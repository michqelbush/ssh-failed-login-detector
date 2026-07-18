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

## Next steps

I was thinking about the other stuff I could add and what I've seen other people have for theirs. I want to make it read live, instead of it just being once, making it more applicable and realistic to the real world. Also I could flag it and give a more serious response if after a bunch of failed login attempts they actually get into the account.
