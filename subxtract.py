import os
import threading
import time

subfinder_file = ""
assetfinder_file = ""
findomain_file = ""

def get_parent_domain(domain, original_domain):
    parts = domain.split('.')
    if len(parts) <= original_domain.count('.') + 1:
        return None
    return '.'.join(parts[1:])

    
def findomain(domain):
    global findomain_file
    subdomain_set = {domain}
    processed_domains = set()
    directory = "findomain_sub_"+domain+".txt"
    findomain_file = directory
    while subdomain_set:
    	current_domain = subdomain_set.pop()
    	if current_domain != domain:
    		parent_domain = get_parent_domain(current_domain,domain)
    		if parent_domain is not None:
    			subdomain_set.add(parent_domain)
    	if current_domain in processed_domains:
    		continue
    	os.system(f"findomain -t {current_domain} -q >> {directory} 2>/dev/null")
    	processed_domains.add(current_domain)
    	with open(directory, "r") as f:
    	    for line in f:
                string = line.strip()
                if string.endswith("."):
                    string = string[:-1]
                if string not in processed_domains:
                    subdomain_set.add(string)

def assetfinder(domain):
    global assetfinder_file  
    subdomain_set = {domain}
    processed_domains = set()
    directory = "asset_sub_"+domain+".txt"
    assetfinder_file = directory
    while subdomain_set:
        current_domain = subdomain_set.pop()
        if current_domain != domain:
        	parent_domain = get_parent_domain(current_domain,domain)
        	if parent_domain is not None:
        		subdomain_set.add(parent_domain)
        if current_domain in processed_domains:
            continue
        os.system(f"assetfinder -subs-only {current_domain} >> {directory} 2>/dev/null")
        processed_domains.add(current_domain)
        with open(directory, "r") as f:
            for line in f:
                string = line.strip()
                if string.endswith("."):
                    string = string[:-1]
                if string not in processed_domains:
                    subdomain_set.add(string)

def subfinder(domain):
    global subfinder_file  
    subdomain_set = {domain}
    processed_domains = set()
    directory = "subfinder_sub_"+domain+".txt"
    subfinder_file = directory

    while subdomain_set:
        current_domain = subdomain_set.pop()
        if current_domain != domain:
        	parent_domain = get_parent_domain(current_domain,domain)
        	if parent_domain is not None:
        		subdomain_set.add(parent_domain)
        if current_domain in processed_domains:
            continue
        os.system(f"subfinder -d {current_domain} -silent >> {directory} 2>/dev/null")  
        processed_domains.add(current_domain)

        with open(directory, "r") as f:
            for line in f:
                string = line.strip()
                if string.endswith("."):
                    string = string[:-1]
                if string not in processed_domains:
                    subdomain_set.add(string)

input_domain = input("Enter your domain for subdomain enumeration: ")

t1 = threading.Thread(target=assetfinder, args=(input_domain,))
t2 = threading.Thread(target=subfinder, args=(input_domain,))
t3 = threading.Thread(target=findomain, args=(input_domain,))

print(f"[+] Starting the subdomain enumeration of {input_domain}..")
time.sleep(1)
print("[+] It is a recursive subdomain enumeration, i.e., this script finds the subdomains of the subdomains until there is no one left...")
time.sleep(1)
print("[+] It will take some time... So Sit back and Relax...")
time.sleep(1)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

print("[+] The subdomain enumeration has been completed..")

if subfinder_file and assetfinder_file and findomain_file: 
    os.system(f"cat {subfinder_file} >> {assetfinder_file}")
    os.system(f"cat {findomain_file} >> {assetfinder_file}")
    os.system(f"mv {assetfinder_file} clean_subs_{input_domain}.txt")
    os.system(f"rm {subfinder_file} {findomain_file}")
    os.system(f"sort clean_subs_{input_domain}.txt -u > clean__subs_{input_domain}.txt")
    os.system(f"rm clean_subs_{input_domain}.txt")
    print("\nThank you for using the script...")
else:
    print("[-] Error: Subdomain enumeration files were not created properly.")