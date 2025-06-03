import os

input_domain = input("Enter your domain for subdomain enumeration:")
subdomain_set = {input_domain}
processed_domains = set()
directory = "sub_"+input_domain+".txt"

while subdomain_set:
    current_domain = subdomain_set.pop()
    if current_domain in processed_domains:
        continue
        
    print(f"[+] Finding the subdomains for {current_domain}...")
    os.system(f"subfinder -d {current_domain} -silent -all >> {directory}")
    os.system(f"assetfinder -subs-only {current_domain} >> {directory}")
    print(f"[+] Subdomains found successfully for {current_domain}...\n")
    
    processed_domains.add(current_domain)
    
    with open(directory, "r") as f:
        for line in f:
            string = line.strip()
            if string.endswith("."): 
                string = string[:-1]
            if string not in processed_domains:
                subdomain_set.add(string)

os.system(f"cat {directory} | sort -u >> clean_sub_{input_domain}.txt")
os.system(f"rm {directory}")

ch = input("Do you want to perform the live subdomain detection?? (y or n)")
if ch == 'y':
    os.system(f"httpx -l clean_sub_{input_domain}.txt -sc -title -tech-detect -o live_info_{input_domain}.txt")
print("\n\n\nThank you for using the script...")