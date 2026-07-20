import re
import argparse
import subprocess
from collections import Counter

def block_ip(ip):
	subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)

def parse_auth_log(log_path, threshold, block):
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
		if count >= threshold and block:
			print(f"{ip} over threshold, blocked via iptables")
			block_ip(ip)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Parse SSH auth logs for failed attempst.")
	parser.add_argument("logfile", nargs="?", default="/var/log/auth.log", help="Path to auth log file")
	parser.add_argument("--threshold", type=int, default=3, help="Failed attempts before flagging as SUS")
	parser.add_argument("--block", action="store_true", help="Actually block flagged IPs using iptables")
	args = parser.parse_args()

	parse_auth_log(args.logfile, args.threshold, args.block)
