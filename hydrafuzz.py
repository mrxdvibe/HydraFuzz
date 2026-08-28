#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
   ██╗  ██╗██╗   ██╗██████╗ ██████╗  █████╗ ███████╗██╗   ██╗███████╗███████╗
   ██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██║   ██║╚══███╔╝╚══███╔╝
   ███████║ ╚████╔╝ ██║  ██║██████╔╝███████║█████╗  ██║   ██║  ███╔╝   ███╔╝ 
   ██╔══██║  ╚██╔╝  ██║  ██║██╔══██╗██╔══██║██╔══╝  ██║   ██║ ███╔╝   ███╔╝  
   ██║  ██║   ██║   ██████╔╝██║  ██║██║  ██║██║     ╚██████╔╝███████╗███████╗
   ╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚══════╝
================================================================================
                 Hybrid Dynamic Reconnaissance & Algorithmic Fuzzer
                         Developer: MrxdVibe | PhantomSec
================================================================================
"""

import sys
import argparse
import asyncio
import time
import urllib3
import aiohttp
from colorama import Fore, Style, init
from generator import PermutationEngine
from spider import HydraSpider

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

BANNER = f"""{Fore.CYAN}{Style.BRIGHT}
  ██╗  ██╗██╗   ██╗██████╗ ██████╗  █████╗ ███████╗██╗   ██╗███████╗███████╗
  ██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██║   ██║╚══███╔╝╚══███╔╝
  ███████║ ╚████╔╝ ██║  ██║██████╔╝███████║█████╗  ██║   ██║  ███╔╝   ███╔╝ 
  ██╔══██║  ╚██╔╝  ██║  ██║██╔══██╗██╔══██║██╔══╝  ██║   ██║ ███╔╝   ███╔╝  
  ██║  ██║   ██║   ██████╔╝██║  ██║██║  ██║██║     ╚██████╔╝███████╗███████╗
  ╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚══════╝
{Fore.MAGENTA}================================================================================
{Fore.WHITE}{Style.BRIGHT}   [+] Enterprise Dynamic Reconnaissance & Algorithmic Fuzzer
   [+] Team   : {Fore.YELLOW}Phantom Cyber Research (PhantomSec)
{Fore.WHITE}   [+] Author : {Fore.CYAN}MrxdVibe
{Fore.WHITE}   [+] Engine : {Fore.GREEN}v2.0 Elite (Wordlist-Free / Interactive Loop)
{Fore.MAGENTA}================================================================================{Style.RESET_ALL}
"""

STATUS_COLORS = {
    200: Fore.GREEN + Style.BRIGHT,
    301: Fore.BLUE + Style.BRIGHT,
    302: Fore.BLUE + Style.BRIGHT,
    401: Fore.YELLOW + Style.BRIGHT,
    403: Fore.RED + Style.BRIGHT,
    500: Fore.MAGENTA + Style.BRIGHT
}

class HydraFuzzEngine:
    def __init__(self, target_url, concurrency=30, timeout=2, output_file=None):
        self.target_url = target_url.rstrip('/')
        if not self.target_url.startswith(('http://', 'https://')):
            self.target_url = 'http://' + self.target_url
        
        self.concurrency = concurrency
        self.timeout = timeout
        self.output_file = output_file
        self.found_results = []
        self.scanned_count = 0

    async def fetch(self, session, path, semaphore, total_payloads):
        url = f"{self.target_url}/{path.lstrip('/')}"
        async with semaphore:
            try:
                # Agressiv 2 saniyəlik timeout (1 saniyə qoşulma limiti ilə)
                client_timeout = aiohttp.ClientTimeout(total=self.timeout, connect=1)
                async with session.get(url, timeout=client_timeout, allow_redirects=False, ssl=False) as response:
                    status = response.status
                    self.scanned_count += 1
                    
                    if status in [200, 301, 302, 401, 403, 500]:
                        color = STATUS_COLORS.get(status, Fore.WHITE)
                        status_str = f"[{color}{status}{Style.RESET_ALL}]"
                        length = response.headers.get('Content-Length', 'N/A')
                        
                        log_msg = f"{status_str} {Fore.WHITE}{url}{Style.RESET_ALL} (Size: {length})"
                        print(f" {Fore.GREEN}➔{Style.RESET_ALL} {log_msg}", flush=True)
                        self.found_results.append((status, url, length))
            except Exception:
                self.scanned_count += 1

    async def run(self):
        print(f"\n{Fore.CYAN}[*] Hədəf URL       :{Style.RESET_ALL} {Fore.WHITE}{self.target_url}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Asinxron Yiv   :{Style.RESET_ALL} {Fore.WHITE}{self.concurrency} Paralel Sorğu{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Çıxış Faylı     :{Style.RESET_ALL} {Fore.WHITE}{self.output_file if self.output_file else 'Yoxdur'}{Style.RESET_ALL}\n")

        print(f"{Fore.YELLOW}[*] FAZA 1: Dynamic Crawler (Hörümçək Mühərriki) İşə Düşür...{Style.RESET_ALL}")
        spider = HydraSpider(self.target_url)
        crawled_words, endpoints = spider.crawl()
        print(f" {Fore.GREEN}✔{Style.RESET_ALL} Saytdan tapılan söz sayı     : {Fore.GREEN}{len(crawled_words)}{Style.RESET_ALL}")
        print(f" {Fore.GREEN}✔{Style.RESET_ALL} Tapılan daxili endpoint sayı : {Fore.GREEN}{len(endpoints)}{Style.RESET_ALL}\n")

        print(f"{Fore.YELLOW}[*] FAZA 2: Permutation Engine (Dinamik Generator) İşə Düşür...{Style.RESET_ALL}")
        gen = PermutationEngine(self.target_url)
        payloads = set(gen.generate(base_words=crawled_words))
        
        for ep in endpoints:
            payloads.add(ep.lstrip('/'))

        total_payloads = len(payloads)
        print(f" {Fore.GREEN}✔{Style.RESET_ALL} Ümumi dinamik ehtimal sayısı : {Fore.GREEN}{total_payloads}{Style.RESET_ALL}\n")

        print(f"{Fore.YELLOW}[*] FAZA 3: High-Speed Async Fuzzing Başlayır...{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}" + "─"*70 + f"{Style.RESET_ALL}")

        start_time = time.time()
        semaphore = asyncio.Semaphore(self.concurrency)
        headers = {
            'User-Agent': 'Mozilla/5.0 (HydraFuzz/2.0 Elite Recon Engine)',
            'Accept': '*/*'
        }

        conn = aiohttp.TCPConnector(limit=self.concurrency, ssl=False)
        async with aiohttp.ClientSession(headers=headers, connector=conn) as session:
            tasks = [self.fetch(session, payload, semaphore, total_payloads) for payload in payloads]
            
            # as_completed istifadə edilərək nəticəsi gələn sorğu dərhal ekrana basılır
            for task in asyncio.as_completed(tasks):
                await task

        elapsed_time = round(time.time() - start_time, 2)
        
        print(f"{Fore.MAGENTA}" + "─"*70 + f"{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}[+] SKAN NƏTİCƏSİ XÜLASƏSİ{Style.RESET_ALL}")
        print(f" {Fore.GREEN}✔{Style.RESET_ALL} Keçən Vaxt          : {Fore.WHITE}{elapsed_time} saniyə{Style.RESET_ALL}")
        print(f" {Fore.GREEN}✔{Style.RESET_ALL} Yoxlanılan Ehtimal : {Fore.WHITE}{self.scanned_count}{Style.RESET_ALL}")
        print(f" {Fore.GREEN}✔{Style.RESET_ALL} Tapılan Kritik Yol : {Fore.GREEN}{len(self.found_results)}{Style.RESET_ALL}")

        if self.output_file and self.found_results:
            try:
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    f.write(f"HydraFuzz v2.0 Scan Report for {self.target_url}\n")
                    f.write("="*60 + "\n")
                    for status, url, length in self.found_results:
                        f.write(f"[{status}] {url} (Size: {length})\n")
                print(f"\n{Fore.GREEN}[+] Nəticələr müvəffəqiyyətlə '{self.output_file}' faylına yazıldı!{Style.RESET_ALL}")
            except Exception as e:
                print(f"\n{Fore.RED}[-] Fayla yazarkən xəta baş verdi: {e}{Style.RESET_ALL}")

def interactive_menu():
    while True:
        print(BANNER)
        print(f"{Fore.YELLOW}[+] SKAN REJİMİNİ SEÇİN:{Style.RESET_ALL}\n")
        print(f"  {Fore.GREEN}[1]{Style.RESET_ALL}  {Fore.WHITE}Sadə / Standart Skan{Style.RESET_ALL}     (15 Paralel Sorğu - Güvənli)")
        print(f"  {Fore.GREEN}[2]{Style.RESET_ALL}  {Fore.WHITE}Yüksək Sürətli Skan{Style.RESET_ALL}      (50 Paralel Sorğu - Ultra Sürətli)")
        print(f"  {Fore.GREEN}[3]{Style.RESET_ALL}  {Fore.WHITE}Aqressiv Turbo Skan{Style.RESET_ALL}      (100 Paralel Sorğu - Maksimum Sürət)")
        print(f"  {Fore.RED}[0]{Style.RESET_ALL}  {Fore.WHITE}Çıxış{Style.RESET_ALL}\n")

        choice = input(f"{Fore.CYAN}Seçiminiz (1/2/3/0) ➔ {Style.RESET_ALL}").strip()

        if choice == '0':
            print(f"\n{Fore.RED}[!] Proqramdan çıxılır...{Style.RESET_ALL}")
            sys.exit(0)

        concurrency_map = {'1': 15, '2': 50, '3': 100}
        concurrency = concurrency_map.get(choice, 30)

        target_url = input(f"\n{Fore.CYAN}Hədəf Saytı Daxil Edin (məs: http://zero.webappsecurity.com) ➔ {Style.RESET_ALL}").strip()
        if not target_url:
            print(f"{Fore.RED}[!] Xəta: Hədəf URL boş ola bilməz!{Style.RESET_ALL}\n")
            continue

        save_choice = input(f"{Fore.CYAN}Nəticələr fayla yazılsın? (y/n) [n] ➔ {Style.RESET_ALL}").strip().lower()
        output_file = None
        if save_choice in ['y', 'yes', 'bəli', 'b']:
            output_file = input(f"{Fore.CYAN}Fayl adı (defolt: results.txt) ➔ {Style.RESET_ALL}").strip()
            if not output_file:
                output_file = "results.txt"

        engine = HydraFuzzEngine(
            target_url=target_url,
            concurrency=concurrency,
            output_file=output_file
        )
        asyncio.run(engine.run())

        print("\n" + f"{Fore.YELLOW}" + "="*70 + f"{Style.RESET_ALL}")
        again = input(f"{Fore.CYAN}Yenidən yeni skan etmək istəyirsiniz? (y/n) [y] ➔ {Style.RESET_ALL}").strip().lower()
        if again in ['n', 'no', 'xeyr', 'x']:
            print(f"\n{Fore.RED}[!] PhantomSec HydraFuzz dayandırıldı. Uğurlar!{Style.RESET_ALL}\n")
            break
        print("\n" * 2)

def main():
    parser = argparse.ArgumentParser(description="HydraFuzz - Enterprise Dynamic Reconnaissance & Algorithmic Fuzzer")
    parser.add_argument("-u", "--url", help="Hədəf Sayt / Domen")
    parser.add_argument("-t", "--threads", type=int, default=30, help="Paralel asinxron sorğu sayısı")
    parser.add_argument("-o", "--output", help="Nəticələrin saxlanılacağı fayl adı")
    
    args = parser.parse_args()

    if args.url:
        engine = HydraFuzzEngine(
            target_url=args.url,
            concurrency=args.threads,
            output_file=args.output
        )
        asyncio.run(engine.run())
    else:
        interactive_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Skan istifadəçi tərəfindən dayandırıldı.{Style.RESET_ALL}")
        sys.exit(0)
