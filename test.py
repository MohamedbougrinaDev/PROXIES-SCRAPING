import requests
import os
from colorama import Fore
import pyfiglet
import threading
from concurrent.futures import ThreadPoolExecutor

R = Fore.RED 
Y = Fore.YELLOW
G = Fore.GREEN
W = Fore.WHITE
C = Fore.CYAN

class Settings:
    def logo():
        print(C + pyfiglet.figlet_format("P R O X I E S"))
    
    def clear():
        os.system("clear")
    
    def add_to(filename="working_proxies.txt", text=None):
        with open(filename, "a") as file:
            file.write(text + "\n")
    
    def check_proxy(proxy):
        try:
            proxy = proxy.strip()
            if not proxy:
                return None
                
            parts = proxy.split(":")
            if len(parts) < 2:
                return None
                
            ip = parts[0]
            port = parts[1]
            proxies_data = {
                "http": f"http://{ip}:{port}",
                "https": f"http://{ip}:{port}"
            }
            
            response = requests.get(
                "http://httpbin.org/ip",
                proxies=proxies_data,
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            if response.status_code == 200:
                result = response.json()
                proxy_ip = result['origin'].split(',')[0]
                print(f"{G}✓ Working proxy: {W}{ip}:{port}")
                Settings.add_to(text=f"{ip}:{port}")
                return f"{ip}:{port}"
            else:
                print(f"{R}✗ Failed: {W}{ip}:{port}")
                return None
                
        except Exception:
            print(f"{R}✗ Failed: {W}{proxy.split(':')[0]}:{proxy.split(':')[1]}")
            return None
    
    def scanning_proxies(data):
        working_proxies = []
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(Settings.check_proxy, data)
            
        working_proxies = [result for result in results if result is not None]
        
        print(f"\n{G}Scanning completed!{W}")
        print(f"{G}Working proxies: {len(working_proxies)}{W}")
        print(f"{G}Saved to: working_proxies.txt{W}")
        
        return working_proxies
    
    def getproxies():
        try:
            all_proxies = []
            sources = [
                "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
                "https://www.proxy-list.download/api/v1/get?type=http",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
            ]
            
            for source in sources:
                print(f"{Y}Requesting URL: {W}{source}")
                try:
                    response = requests.get(source, timeout=10)
                    if response.status_code == 200:
                        proxies = response.text.strip().split('\n')
                        all_proxies.extend([proxy.strip() for proxy in proxies if proxy.strip()])
                        print(f"{G}Found {len(proxies)} proxies from {source}")
                    else:
                        print(f"{R}Failed to fetch from {source} - Status: {response.status_code}")
                except Exception as source_error:
                    print(f"{R}Error fetching from {source}: {str(source_error)}")
            
            return list(set(all_proxies))
            
        except Exception as error:
            print(f"{R}Error in getproxies: {error}")
            return []

if __name__ == "__main__":
    os.system("clear")
    Settings.logo()
    proxies = Settings.getproxies()
    print(f"{C}Total proxies found: {len(proxies)}{W}")
    
    if proxies:
        print(f"{Y}Scanning all proxies with threading...{W}\n")
        working = Settings.scanning_proxies(proxies)