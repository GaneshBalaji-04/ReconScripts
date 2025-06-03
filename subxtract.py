import os

input_domain = input("Enter your domain for subdomain enumeration:")
subdomain_set = {input_domain}
directory = "sub_"+input_domain+".txt"

while subdomain_set:
    current_domains = list(subdomain_set.copy())
    for domain in current_domains:
        print(f"[+] Finding the subdomains for {domain}...")
        os.system(f"subfinder -d {domain} -silent -all >> {directory}")
        os.system(f"assetfinder {domain} >> {directory}")
        print(f"[+] Subdomains found successfully for {domain}...\n")
                
        subdomain_set.remove(domain)
        
        with open(directory, "r") as f:
            for line in f:
                string = line.strip()
                if string.endswith("."): 
                    string = string[:-1]
                subdomain_set.add(string)

os.system(f"cat {directory} | sort -u >> clean_sub_{input_domain}.txt")
os.system(f"rm sub_{input_domain}.txt")

ch = input("Do you want to perform the live subdomain detection?? (y or n)")
if ch==y:
	os.system(f"httpx -l clean_sub_{input_domain}.txt -sc -title -tech-detect -o live_info_{input_domain}.txt")
print("\n\n\nThank you for using the script...")