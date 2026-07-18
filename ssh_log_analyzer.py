import re
import argparse
from collections import Counter

def parse_auth_log(log_path, threshold):
	pattern = r"^(\S+) \S+ sshd-session\[\d+\]: Failed password for (\S+) from (\S+) port \d+"
	failures_by_ip = Counter()

	with open(log_path, "r") as f:
		for line in f:
			match = re.search(pattern, line)
			if match:
				timestamp, user, ip = match.groups()
				failures_by_ip[ip] += 1

	print("Failed Login Summary")

	if not failures_by_ip:
		print("No failed login attpts found")
		return

	for ip, count in failures_by_ip.most_common():
		flag = "SUS" if count >= threshold else ""
		print(f"{ip}: {count} failed attempts {flag}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Parse SSH auth logs for failed attempst.")
	parser.add_argument("logfile", nargs="?", default="/var/log/auth.log", help="Path to auth log file")
	parser.add_argument("--threshold", type=int, default=3, help="Failed attempts before flagging as SUS")
	args = parser.parse_args()

	parse_auth_log(args.logfile, args.threshold)
