import os

domain = input("Enter your domain for subdomain enumeration:")
subdomain_set = {domain}
final_destination_directory = domain + "_all_subdomains.txt"
num = 0

while subdomain_set:
    current_domains = list(subdomain_set.copy())
    for domain in current_domains:
        directory = f"_subdomain_{num}.txt"
        num += 1
        print(f"[+] Finding the subdomains for {domain}...")
        os.system(f"subfinder -d {domain} -o {directory} -silent > /dev/null")
        print(f"[+] Subdomains found successfully for {domain}...\n")
        
        subdomain_set.remove(domain)
        
        with open(directory, "r") as f:
            for line in f:
                string = line.strip()
                if string.endswith("."): 
                    string = string[:-1]
                subdomain_set.add(string)

os.system(f"cat _subdomain* | sort -u > {final_destination_directory}")
os.system("rm _subdomain*")