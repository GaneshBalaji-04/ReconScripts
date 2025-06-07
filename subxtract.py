import os
import threading
import time

subfinder_file = ""
assetfinder_file = ""
findomain_file = ""

def findomain(domain):
    global findomain_file
    subdomain_set = {domain}
    processed_domains = set()
    directory = "findomain_sub_"+domain+".txt"
    findomain_file = directory
    while subdomain_set:
    	current_domain = subdomain_set.pop()
    	domain_ = current_domain.split(".")
    	domain_.remove(domain_[0])
    	parent_domain = domain_[0]
    	for i in range(1,len(domain_)):
    		parent_domain = parent_domain + "." + domain_[i]
    	subdomain_set.add(parent_domain)
    	if current_domain in processed_domains:
    		continue
    	os.system(f"findomain -t {current_domain} -q >> {directory}")
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
        domain_ = current_domain.split(".")
        domain_.remove(domain_[0])
        parent_domain = domain_[0]
        for i in range(1,len(domain_)):
        	parent_domain = parent_domain + "." + domain_[i]
        subdomain_set.add(parent_domain)
        if current_domain in processed_domains:
            continue
        os.system(f"assetfinder -subs-only {current_domain} >> {directory}")
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
        domain_ = current_domain.split(".")
        domain_.remove(domain_[0])
        parent_domain = domain_[0]
        for i in range(1,len(domain_)):
        	parent_domain = parent_domain + "." + domain_[i]
        subdomain_set.add(parent_domain)
        if current_domain in processed_domains:
            continue
        os.system(f"subfinder -d {current_domain} -silent >> {directory}")  
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

print(f"[+] Starting the subdomain enumeration of {input_domain}..")  # Fixed missing f-string
time.sleep(0.5)  # Fixed: time.delay() doesn't exist, should be time.sleep()
print("[+] It is a recursive subdomain enumeration, i.e., this script finds the subdomains of the subdomains until there is no one left...")
time.sleep(0.5)
print("[+] It will take some time... So Sit back and Relax...")
time.sleep(0.5)

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
    os.system(f"cat {assetfinder_file} | sort -u >> clean_sub_{input_domain}.txt")
    os.system(f"rm {subfinder_file} {assetfinder_file} {findomain_file}")
    print("[+] Performing Live subdomains discovery...")
    os.system(f"naabu -l clean_sub_{input_domain}.txt -p- -Pn -o live_{input_domain}.txt > /dev/null")
    os.system(f"httpx -l live_{input_domain}.txt -sc -title -tech-detect -o live_info_{input_domain}.txt")
    print("[+] Live subdomains discovery completed...")
    print("\nThank you for using the script...")
else:
    print("[-] Error: Subdomain enumeration files were not created properly.")