import requests
from concurrent.futures import ThreadPoolExecutor


domain="google.com"
discovered_subdomains=[]

with open("subdomain.txt") as file:
    subdomains=file.read().splitlines()


def check_subdomain(subdomain):
    protocols=['http','https']
    for protocol in protocols:
        url=f"{protocol}://{subdomain}.{domain}"
        try:
            response=requests.get(url,timeout=2)
            if response.status_code==200:
                print("[+]Discovered subdomain:",url)
                discovered_subdomains.append(url)
                break

        except requests.ConnectionError:
            pass

        except requests.Timeout:
            print(f"[-] Timeout for {url}")

        except requests.RequestException as e:
            print(f"[-] Failed for {url}:{e}")

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(check_subdomain,subdomains)


with open("discovered_subdomains.txt","w") as f:
    for subdomain in discovered_subdomains:
        print(subdomain,file=f)


