import requests
from bs4 import BeautifulSoup
import time
import threading
from queue import Queue
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn, TimeElapsedColumn
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
import os
import sys

console = Console()

class EliteProxyScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.proxy_list = []
        self.live_proxies = []
        self._sources = [
            'https://www.sslproxies.org/',
            'https://free-proxy-list.net/',
            'https://www.us-proxy.org/',
            'https://www.proxy-list.download/HTTP',
            'https://www.hide-my-ip.com/proxylist.shtml',
            'https://proxyscrape.com/free-proxy-list',
            'https://openproxy.space/list/http',
            'https://www.freeproxylists.net/',
            'https://www.proxynova.com/proxy-server-list/',
            'https://www.proxy-daily.com/',
            'https://spys.one/en/free-proxy-list/',
            'https://www.my-proxy.com/free-proxy-list.html',
            'https://proxy11.com/free-proxy/',
            'https://www.freeproxy.world/',
            'https://www.live-proxy.net/',
            'https://www.proxy-listen.de/Proxy/Proxyliste.html',
            'https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc',
            'https://www.cool-proxy.net/proxies.json',
            'https://www.proxyscan.io/api/proxy?format=json&limit=100',
            'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
            'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
            'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
            'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
            'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt',
            'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS.txt',
            'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
            'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt',
            'https://www.proxy-list.download/api/v1/get?type=http',
            'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all',
            'https://www.proxydocker.com/en/proxylist/api?format=txt',
            'https://proxylist.me/api/proxies?type=http&limit=50',
            'https://www.freeproxychecker.com/api/proxy/list?page=1&limit=100',
            'https://proxyhub.me/en/all-active-free-proxy-list.html',
            'https://www.proxypedia.org/',
            'https://www.proxyrack.com/free-proxies/',
            'https://www.idcloak.com/proxylist/free-proxy-list.html',
            'https://www.proxylists.net/http.txt',
            'https://www.proxy4free.com/en/proxy-list/',
            'https://www.freshproxylist.org/',
            'https://www.proxyserverlist24.top/',
            'https://proxylist.live/free-proxy-list/',
            'https://www.blackhatworld.com/seo/proxy-list.1128439/',
            'https://www.freeproxylist.cc/',
            'https://www.hidemy.name/en/proxy-list/',
            'https://www.proxy-list.org/english/index.php',
            'https://www.proxylistpro.com/free-proxies/',
            'https://www.luxproxy.com/free-proxy-list/',
            'https://www.multiproxy.org/txt_all/proxy.txt',
            'https://www.samair.ru/proxy/proxy-01.htm',
            'https://www.proxz.com/proxy_list_high_anonymous_0.html',
            'https://www.proxyelite.info/en/free-proxy-list/',
            'https://www.httptunnel.ge/ProxyListForFree.aspx',
            'https://www.getproxy.io/free-proxies/',
            'https://www.proxyranker.com/free-proxy-list/',
            'https://www.proxyway.com/free-proxy-list/'
        ]
        self.stats = {'total_collected': 0, 'live_count': 0, 'dead_count': 0, 'sources_used': 0}

    def clear_screen(self):
        """Xóa màn hình triệt để"""
        console.clear()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" * 50)

    def typing_effect(self, text, delay=0.05):
        """Hiệu ứng gõ chữ"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def test_connection(self):
        """Kiểm tra kết nối mạng"""
        self.clear_screen()
        console.print(Align.center(Panel("[yellow bold]Đang kiểm tra kết nối mạng...[/yellow bold]", border_style="yellow", width=70, padding=(1, 1))))
        try:
            requests.get('https://www.google.com', timeout=5)
            console.print(Align.center(Panel("[green bold]✓ Kết nối mạng ổn định![/green bold]", border_style="green1", width=70, padding=(1, 1))))
            time.sleep(1)
            return True
        except requests.RequestException:
            console.print(Align.center(Panel("[red bold]✗ Không có kết nối mạng![/red bold]", border_style="red", width=70, padding=(1, 1))))
            time.sleep(2)
            return False

    def scrape_from_source(self, source_index, limit=None):
        """Thu thập proxy từ nguồn"""
        url = self._sources[source_index]
        proxies = []
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            content_type = response.headers.get('Content-Type', '').lower()

            if 'html' in content_type:
                soup = BeautifulSoup(response.text, 'html.parser')
                proxy_table = soup.find('table')
                if proxy_table:
                    for row in proxy_table.find_all('tr')[1:]:
                        if limit is not None and len(proxies) >= limit:
                            break
                        cols = row.find_all('td')
                        if len(cols) >= 2:
                            ip = cols[0].text.strip()
                            port = cols[1].text.strip()
                            proxy = f"{ip}:{port}"
                            if proxy not in proxies and ip and port:
                                proxies.append(proxy)
                else:
                    text = soup.get_text()
                    for line in text.splitlines():
                        if limit is not None and len(proxies) >= limit:
                            break
                        parts = line.strip().split(':')
                        if len(parts) == 2 and parts[0].count('.') == 3 and parts[1].isdigit():
                            proxy = f"{parts[0]}:{parts[1]}"
                            if proxy not in proxies:
                                proxies.append(proxy)

            elif 'text' in content_type or 'json' in content_type:
                if 'json' in content_type:
                    data = response.json()
                    if isinstance(data, list):
                        for item in data:
                            if limit is not None and len(proxies) >= limit:
                                break
                            if 'ip' in item and 'port' in item:
                                proxy = f"{item['ip']}:{item['port']}"
                                if proxy not in proxies:
                                    proxies.append(proxy)
                else:
                    for line in response.text.splitlines():
                        if limit is not None and len(proxies) >= limit:
                            break
                        parts = line.strip().split(':')
                        if len(parts) == 2 and parts[0].count('.') == 3 and parts[1].isdigit():
                            proxy = f"{parts[0]}:{parts[1]}"
                            if proxy not in proxies:
                                proxies.append(proxy)

            self.stats['sources_used'] += 1
            console.print(f"[green]✓ Thu thập: {len(proxies)} proxy từ nguồn {source_index + 1}[/green]")
            return proxies
        except Exception as e:
            console.print(f"[red bold]✗ Lỗi tại nguồn {source_index + 1}: {str(e)}[/red bold]")
            return []

    def check_proxy(self, proxy, queue):
        """Kiểm tra proxy sống"""
        try:
            requests.get('https://www.google.com', 
                        proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'}, 
                        timeout=5)
            queue.put((proxy, True))
        except:
            queue.put((proxy, False))

    def collect_and_check_proxies(self, target_count):
        """Thu thập và kiểm tra proxy"""
        if not self.test_connection():
            return

        self.clear_screen()
        self.proxy_list = []
        self.live_proxies = []
        self.stats = {'total_collected': 0, 'live_count': 0, 'dead_count': 0, 'sources_used': 0}
        remaining = target_count
        start_time = time.time()

        with Progress(
            SpinnerColumn(style="cyan"),
            TextColumn("[bold white]{task.description}"),
            BarColumn(bar_width=None, style="green1", complete_style="bright_green"),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task(f"Đang thu thập {target_count} proxy", total=len(self._sources))
            for i in range(len(self._sources)):
                if len(self.proxy_list) >= target_count:
                    break
                limit = remaining if remaining > 0 else None
                proxies = self.scrape_from_source(i, limit)
                self.proxy_list.extend(proxies)
                self.stats['total_collected'] += len(proxies)
                self.proxy_list = list(set(self.proxy_list))[:target_count]
                remaining = target_count - len(self.proxy_list)
                progress.update(task, advance=1)
                time.sleep(2)

        if self.proxy_list:
            console.print(f"\n[cyan]Đang kiểm tra {len(self.proxy_list)} proxy...[/cyan]")
            queue = Queue()
            threads = []
            for proxy in self.proxy_list:
                t = threading.Thread(target=self.check_proxy, args=(proxy, queue))
                t.start()
                threads.append(t)
            
            with Progress(
                SpinnerColumn(style="cyan"),
                TextColumn("[bold white]Kiểm tra proxy...[/bold white]"),
                BarColumn(bar_width=None, style="blue1", complete_style="bright_blue"),
                "[progress.percentage]{task.percentage:>3.0f}%",
                TimeElapsedColumn(),
                console=console
            ) as progress:
                task = progress.add_task("Kiểm tra", total=len(self.proxy_list))
                for _ in range(len(self.proxy_list)):
                    proxy, alive = queue.get()
                    if alive:
                        self.live_proxies.append(proxy)
                        self.stats['live_count'] += 1
                    else:
                        self.stats['dead_count'] += 1
                    progress.update(task, advance=1)

            for t in threads:
                t.join()

            elapsed_time = time.time() - start_time
            stats_table = Table(title="Thống kê", show_lines=True, width=70, border_style="green1")
            stats_table.add_column("Thông tin", style="cyan bold")
            stats_table.add_column("Giá trị", style="green1")
            stats_table.add_row("Tổng proxy thu thập", str(self.stats['total_collected']))
            stats_table.add_row("Proxy sống", str(self.stats['live_count']))
            stats_table.add_row("Proxy chết", str(self.stats['dead_count']))
            stats_table.add_row("Nguồn đã sử dụng", str(self.stats['sources_used']))
            stats_table.add_row("Thời gian thực thi", f"{elapsed_time:.2f} giây")

            console.print(Align.center(Panel(stats_table, title="Kết quả Thu thập", border_style="cyan", padding=(1, 1))))

    def show_proxies(self):
        """Hiển thị proxy sống trong trang mới"""
        self.clear_screen()
        console.print(Align.center(Panel("[cyan bold]Trình xem Proxy sống[/cyan bold]", border_style="cyan", width=70, padding=(1, 1))))
        
        if not self.live_proxies:
            console.print(Align.center(Panel("[yellow bold]⚠ Không có proxy sống nào![/yellow bold]", border_style="yellow", width=70, padding=(1, 1))))
            return

        table = Table(title="Danh sách Proxy Sống", show_lines=True, expand=False, 
                     header_style="bold cyan", border_style="blue1", width=70)
        table.add_column("STT", style="magenta bold", justify="center", width=5)
        table.add_column("Proxy", style="green1", width=35)
        table.add_column("Trạng thái", style="green1", justify="center", width=15)
        
        for i, proxy in enumerate(self.live_proxies[:min(10, len(self.live_proxies))], 1):
            table.add_row(str(i), proxy, "[green]Sống[/green]")
        
        console.print(Align.center(Panel(table, title="Danh sách Proxy", border_style="cyan", padding=(1, 1))))

    def save_proxies(self):
        """Lưu proxy sống"""
        self.clear_screen()
        console.print(Align.center(Panel("[cyan bold]Lưu Proxy Sống[/cyan bold]", border_style="cyan", width=70, padding=(1, 1))))
        
        if not self.live_proxies:
            console.print(Align.center(Panel("[yellow bold]⚠ Không có proxy sống để lưu![/yellow bold]", border_style="yellow", width=70, padding=(1, 1))))
            time.sleep(2)
            return

        console.print(Align.center(Panel(f"[green bold]Hiện có {len(self.live_proxies)} proxy sống[/green bold]", 
                                        border_style="green1", width=70, padding=(1, 1))))
        time.sleep(1)

        if Confirm.ask("\n[bold white]Lưu proxy sống vào file?[/bold white]", console=console, default=True):
            filename = Prompt.ask("[bold cyan]Nhập tên file[/bold cyan]", default="proxy_song.txt", console=console)
            if not filename.endswith('.txt'):
                filename += '.txt'
            
            with Progress(
                SpinnerColumn(style="cyan"),
                TextColumn("[bold white]Đang lưu proxy...[/bold white]"),
                BarColumn(bar_width=None, style="blue1", complete_style="bright_blue"),
                "[progress.percentage]{task.percentage:>3.0f}%",
                console=console
            ) as progress:
                task = progress.add_task("Lưu file", total=len(self.live_proxies))
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        for proxy in self.live_proxies:
                            f.write(proxy + '\n')
                            progress.update(task, advance=1)
                    console.print(Align.center(Panel(f"[bold green]✓ Đã lưu {len(self.live_proxies)} proxy sống vào {filename}[/bold green]", 
                                                    border_style="green1", width=70, padding=(1, 1))))
                except Exception as e:
                    console.print(Align.center(Panel(f"[red bold]✗ Lỗi lưu file: {str(e)}[/red bold]", border_style="red", width=70, padding=(1, 1))))
        else:
            console.print(Align.center(Panel("[blue]Đã bỏ qua việc lưu[/blue]", border_style="blue1", width=70, padding=(1, 1))))
        time.sleep(2)

    def display_menu(self):
        """Hiển thị menu chính với chi tiết"""
        self.clear_screen()
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=6),
            Layout(name="main", size=10),
            Layout(name="footer", size=6)
        )

        # Header
        header_text = Text("Elite Proxy Scraper", style="bold cyan on black")
        header_text.append("\nCông cụ thu thập proxy chuyên nghiệp", style="dim cyan on black")
        layout["header"].update(Align.center(Panel(header_text, border_style="cyan", width=70, padding=(1, 1), style="on black")))

        # Main menu
        menu_table = Table(show_header=False, box=None, expand=False, padding=0, show_edge=False, width=50)
        menu_table.add_row("[yellow bold][1][/yellow bold]", "[green]Thu thập & Kiểm tra Proxy[/green]")
        menu_table.add_row("[yellow bold][2][/yellow bold]", "[green]Xem Proxy Sống[/green]")
        menu_table.add_row("[yellow bold][3][/yellow bold]", "[red]Thoát[/red]")
        layout["main"].update(Align.center(Panel(menu_table, title="[white bold]Lựa chọn[/white bold]", 
                                                border_style="blue1", padding=(2, 2), style="on black")))

        # Footer với bản quyền và trạng thái
        footer_text = Text(f"v1 | Được hỗ trợ bởi SCODE\n© 2025 SCODE Corporation. Bảo lưu mọi quyền.\n", 
                          style="dim white on black", justify="center")
        footer_text.append(f"Trạng thái: {len(self.live_proxies)} proxy sống sẵn có", style="dim green on black")
        layout["footer"].update(Align.center(Panel(footer_text, border_style="cyan", width=70, padding=(1, 1), style="on black")))

        console.print(layout)

    def run(self):
        """Chạy chương trình với trang mới"""
        while True:
            self.display_menu()
            choice = Prompt.ask("[bold yellow]Chọn một tùy chọn[/bold yellow]", choices=["1", "2", "3"], console=console)

            if choice == "1":
                self.clear_screen()
                console.print(Align.center(Panel("[cyan bold]Chế độ Thu thập Proxy[/cyan bold]", border_style="cyan", width=70, padding=(1, 1))))
                target = IntPrompt.ask("[bold cyan]Số lượng proxy cần thu thập[/bold cyan]", default=100, console=console)
                target = max(1, target)
                self.collect_and_check_proxies(target)
                self.show_proxies()
                self.save_proxies()
                Prompt.ask("\n[dim white]Nhấn Enter để tiếp tục[/dim white]", console=console)
                
            elif choice == "2":
                self.show_proxies()
                Prompt.ask("\n[dim white]Nhấn Enter để tiếp tục[/dim white]", console=console)
                
            elif choice == "3":
                self.clear_screen()
                console.print(Align.center(Panel("[bold green]✓ Tạm biệt! Cảm ơn bạn đã sử dụng![/bold green]", 
                                                border_style="green1", width=70, padding=(1, 1))))
                time.sleep(1)
                break

if __name__ == "__main__":
    try:
        console.clear()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" * 50)
        console.print(Align.center(Panel("[yellow bold]Đang khởi động Elite Proxy Scraper...[/yellow bold]", 
                                        border_style="yellow", width=70, padding=(1, 1))))
        time.sleep(1)
        # Hiệu ứng gõ chữ khi khởi động
        console.print("\n")
        console.print(Align.center("[cyan bold]Khởi động công cụ...[/cyan bold]"))
        for i in range(3):
            console.print(Align.center(f"[yellow]{'.' * (i + 1)}[/yellow]"))
            time.sleep(0.5)
        console.clear()
        scraper = EliteProxyScraper()
        scraper.run()
    except KeyboardInterrupt:
        scraper.clear_screen()
        console.print(Align.center(Panel("[red bold]✗ Đã dừng bởi người dùng![/red bold]", border_style="red", width=70, padding=(1, 1))))
        time.sleep(1)
    except Exception as e:
        scraper.clear_screen()
        console.print(Align.center(Panel(f"[red bold]✗ Lỗi: {str(e)}[/red bold]", border_style="red", width=70, padding=(1, 1))))
        time.sleep(1)