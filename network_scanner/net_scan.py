import argparse
from scapy.all import ARP ,Ether ,srp ,conf
import socket
import threading
import csv
import os
from colorama import Fore,Style

def get_mac_vendors(mac):
    mac_prefix=mac[:8].upper()
    vendors={
        "00:1A:2B":"Cisco Systems",
        "00:50:56":"VMware,Inc.",
        "BC:5F:F4":"Dell Inc."

    }
    return vendors.get(mac_prefix,"Unknown Vendor")




def parse_args():
    parser=argparse.ArgumentParser(description="advanced ARp Network scanner")
    parser.add_argument("-t","--target",help="Target IP range(e.g.,192.168.1.1/24)",required=True)
    parser.add_argument("-o", "--output", help="Output file (e.g., scan_results.csv)", default=None)
    parser.add_argument("-to", "--timeout", help="Timeout in seconds (default: 3)", type=int, default=3)
    return parser.parse_args()

def arp_scan(target_ip,timeout=3):
    arp=ARP(pdst=target_ip)
    ether=Ether(dst="ff:ff:ff:ff:ff:ff")
    packet=ether/arp

    print(Fore.YELLOW +f"Scanning the network:{target_ip}..."+ Style.RESET_ALL)
    result=srp(packet,timeout=timeout,verbose=0)[0]

    clients=[]
    for sent,received in result:
        mac=received.hwsrc
        ip=received.psrc
        vendor=get_mac_vendors(mac)
        clients.append({'ip':ip,'mac':mac,'vendor':vendor})

    return clients

def display_results(clients):
    print(Fore.GREEN +"Avaiable devices in the network:" +Style.RESET_ALL)
    print(f"{'IP Address':<20}{'MAC address':<20}{'vendor'}")
    print("-"*50)
    for client in clients:
        print(f"{client['ip']:<20}{client['mac']:<20}{client['vendor']}")


def save_results_to_csv(clients,output_file):
    if output_file:
        with open(output_file,mode='w',newline='') as file:
            writer=csv.writer(file)              
            for client in clients:
                writer.writerow([client['ip'],client['mac'],client['vendor']])
        print(Fore.CYAN + f"results saved to {output_file}" + Style.RESET_ALL)

def run_scan(target_ip,timeout,output_file):
    try:
        clients=arp_scan(target_ip,timeout)
        display_results(clients)
        save_results_to_csv(clients,output_file)


    except PermissionError:
        print(Fore.RED + "[!] Permission Denied.Try running as Adminstartor or using sudo.  " +Style.RESET_ALL)

    except socket.gaierror:
        print(Fore.RED +" [!] Invaild Target IP."+Style.RESET_ALL )

    except Exception as e:
        print(Fore.RED +f"[!] Error occured:{str(e)}" + Style.RESET_ALL)



def main():
    args=parse_args()
    target_ip=args.target
    timeout=args.timeout
    output_file=args.output

    scan_thread=threading.Thread(target=run_scan,args=(target_ip,timeout,output_file))
    scan_thread.start()
    scan_thread.join()



if __name__=="__main__":
    main()


