import subprocess
from concurrent.futures import ThreadPoolExecutor
import os

def run_command(command):
    """Run a shell command and return output lines as list."""
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return [line.strip().rstrip('.') for line in output.splitlines() if line.strip()]
    except subprocess.CalledProcessError:
        return []

def get_parent_domain(domain, original_domain):
    parts = domain.split('.')
    if len(parts) <= original_domain.count('.') + 1:
        return None
    return '.'.join(parts[1:])

def enumerate_tool(domain, tool_name, base_command, recursive=True):
    print(f"[+] Starting {tool_name} on {domain} (recursive={recursive})")

    subdomains = set([domain])
    processed = set()
    results = set()

    while subdomains:
        current = subdomains.pop()
        if current in processed:
            continue

        if recursive and current != domain:
            parent = get_parent_domain(current, domain)
            if parent and parent not in processed:
                subdomains.add(parent)

        command = base_command.format(domain=current)
        found = run_command(command)
        new_subs = set(found) - processed
        results.update(new_subs)
        subdomains.update(new_subs)
        processed.add(current)

    output_file = f"{tool_name}_sub_{domain}.txt"
    with open(output_file, 'w') as f:
        for sub in sorted(results):
            f.write(sub + '\n')
    print(f"[+] {tool_name} completed. Found {len(results)} subdomains.")
    return output_file

def subfinder(domain):
    print(f"[+] Running subfinder on {domain} (non-recursive)")
    results = run_command(f"subfinder -d {domain} -silent 2>/dev/null")
    output_file = f"subfinder_sub_{domain}.txt"
    with open(output_file, 'w') as f:
        for sub in sorted(set(results)):
            f.write(sub + '\n')
    print(f"[+] subfinder completed. Found {len(results)} subdomains.")
    return output_file

def combine_and_deduplicate(files, output_file):
    all_subs = set()
    for file in files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                for line in f:
                    sub = line.strip().rstrip('.')
                    if sub:
                        all_subs.add(sub)
            os.remove(file)
    with open(output_file, 'w') as f:
        for sub in sorted(all_subs):
            f.write(sub + '\n')
    print(f"[+] Final deduplicated output saved to '{output_file}' with {len(all_subs)} unique subdomains.")

if __name__ == "__main__":
    domain = input("Enter your domain for subdomain enumeration: ").strip()
    print(f"\n[+] Starting recursive subdomain enumeration for: {domain}")
    print("[+] Using subfinder (non-recursive) and findomain, assetfinder, amass (recursive)")
    print("[+] Please wait...\n")

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        futures.append(executor.submit(subfinder, domain))
        futures.append(executor.submit(
            enumerate_tool,
            domain,
            "findomain",
            "findomain -t {domain} -q 2>/dev/null"
        ))
        futures.append(executor.submit(
            enumerate_tool,
            domain,
            "assetfinder",
            "assetfinder -subs-only {domain} 2>/dev/null"
        ))
        futures.append(executor.submit(
            enumerate_tool,
            domain,
            "amass",
            "amass enum -d {domain} -o - 2>/dev/null"
        ))

        result_files = [f.result() for f in futures]

    final_output = f"clean__subs_{domain}.txt"
    combine_and_deduplicate(result_files, final_output)
    print("\n[+] Subdomain enumeration completed successfully.")
