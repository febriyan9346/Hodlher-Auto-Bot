import os
import time
import hashlib
import random
from datetime import datetime
import pytz
from colorama import Fore, Style, init
import requests
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct
from typing import Optional, Dict, List
import warnings
import json

os.system('clear' if os.name == 'posix' else 'cls')
warnings.filterwarnings('ignore')

import sys
if not sys.warnoptions:
    os.environ["PYTHONWARNINGS"] = "ignore"

init(autoreset=True)

class HodlHerBot:
    def __init__(self, private_key: str, proxy: Optional[str] = None):
        self.private_key = private_key
        self.proxy = proxy
        self.session = requests.Session()
        self.base_url = "https://dapp.hodlher.ai"
        self.token = None
        self.user_data = None
        
        if self.proxy:
            self.session.proxies = {
                'http': self.proxy,
                'https': self.proxy
            }
        
        self.session.headers.update({
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://dapp.hodlher.ai',
            'referer': 'https://dapp.hodlher.ai/',
            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
        })
        
        self.w3 = Web3()
        self.account = Account.from_key(private_key)
        self.address = self.account.address
        
        self.chat_messages = [
            "Hello! How are you today?",
            "What's your favorite thing to do?",
            "Tell me something interesting!",
            "How has your day been?",
            "What do you think about crypto?",
            "Do you have any hobbies?",
            "What makes you happy?",
            "Tell me a fun fact!",
            "What's on your mind?",
            "How do you feel today?",
            "What are your dreams?",
            "Tell me about yourself!",
            "What do you enjoy most?",
            "Any exciting plans?",
            "What inspires you?"
        ]
    
    def create_signature(self) -> Dict[str, str]:
        timestamp = int(time.time() * 1000)
        address_lower = self.address.lower()
        message = f"Welcome to HodlHer! Please sign this message to verify your wallet ownership.\n\nAddress: {address_lower}\nTimestamp: {timestamp}\nNetwork: BSC"
        
        message_hash = encode_defunct(text=message)
        signed_message = self.account.sign_message(message_hash)
        signature = signed_message.signature.hex()
        
        if not signature.startswith('0x'):
            signature = '0x' + signature
        
        return {
            "address": address_lower,
            "message": message,
            "signature": signature,
            "walletType": "metamask"
        }
    
    def login(self) -> Optional[Dict]:
        try:
            payload = self.create_signature()
            url = f"{self.base_url}/api/auth/signature"
            
            login_headers = self.session.headers.copy()
            login_headers.update({
                'referer': 'https://dapp.hodlher.ai/login',
                'priority': 'u=1, i'
            })
            
            response = self.session.post(url, json=payload, headers=login_headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.token = data.get('token')
                    self.user_data = data.get('user')
                    
                    self.session.headers.update({
                        'authorization': f'Bearer {self.token}'
                    })
                    
                    return data
            return None
        except Exception as e:
            print(f"Login error: {e}")
            return None
    
    def get_user_chats(self, logger) -> Optional[List[Dict]]:
        try:
            if not self.token:
                return None
            
            url = f"{self.base_url}/api/chats"
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('chats', [])
            else:
                logger.log(f"Get chats failed: {response.text}", "ERROR")
                return None
        except Exception as e:
            logger.log(f"Get chats error: {e}", "ERROR")
            return None
    
    def get_chat(self, chat_id: str, logger) -> Optional[Dict]:
        try:
            if not self.token:
                return None
            
            url = f"{self.base_url}/api/chats/{chat_id}"
            
            self.session.headers.update({
                'referer': f'https://dapp.hodlher.ai/talk?chat_id={chat_id}',
                'priority': 'u=1, i'
            })
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.log(f"Get chat failed: {response.text}", "ERROR")
                return None
        except Exception as e:
            logger.log(f"Get chat error: {e}", "ERROR")
            return None
    
    def send_message(self, chat_id: str, message: str, logger) -> Optional[Dict]:
        try:
            if not self.token:
                return None
            
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "chatId": chat_id,
                "is_deep": False,
                "type": "send"
            }
            
            url = f"{self.base_url}/api/chat"
            
            self.session.headers.update({
                'referer': f'https://dapp.hodlher.ai/talk?chat_id={chat_id}',
                'priority': 'u=1, i'
            })
            
            response = self.session.post(url, json=payload, stream=True, timeout=120)
            
            if response.status_code != 200:
                logger.log(f"Send message failed: {response.status_code}", "ERROR")
                return None
            
            full_response = ""
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    if not line.strip():
                        continue
                    
                    if 'data: [DONE]' in line:
                        break
                    
                    if line.startswith('data: '):
                        try:
                            data_str = line[6:]
                            data = json.loads(data_str)
                            if data.get('type') == 'text' and 'content' in data:
                                full_response += data['content']
                        except:
                            continue
            
            return {
                "success": True,
                "response": full_response
            }
            
        except requests.exceptions.Timeout:
            logger.log(f"Request timeout", "ERROR")
            return None
        except Exception as e:
            logger.log(f"Send message error: {e}", "ERROR")
            return None
    
    def do_random_chats_with_existing(self, logger, num_messages: int = 3) -> bool:
        try:
            logger.log(f"Getting existing chats...", "INFO")
            
            chats = self.get_user_chats(logger)
            if not chats or len(chats) == 0:
                logger.log("No existing chats found. Please create a chat manually first!", "WARNING")
                return False
            
            chat_to_use = None
            for chat in chats:
                if chat.get('status'):
                    chat_to_use = chat
                    break
            
            if not chat_to_use:
                chat_to_use = chats[0]
            
            chat_id = chat_to_use['id']
            logger.log(f"Using existing chat: {chat_id[:8]}...", "SUCCESS")
            logger.log(f"Chat title: {chat_to_use.get('title', 'N/A')}", "INFO")
            
            success_count = 0
            for i in range(num_messages):
                logger.log(f"Message #{i+1}/{num_messages}", "INFO")
                
                message = random.choice(self.chat_messages)
                logger.log(f"Sending: '{message}'", "INFO")
                
                send_result = self.send_message(chat_id, message, logger)
                if not send_result or not send_result.get('success'):
                    logger.log(f"Failed to send message", "ERROR")
                else:
                    success_count += 1
                    logger.log(f"Message sent successfully!", "SUCCESS")
                    if 'response' in send_result and send_result['response']:
                        bot_reply = send_result['response']
                        if len(bot_reply) > 150:
                            bot_reply = bot_reply[:150] + "..."
                        logger.log(f"Bot reply: {bot_reply}", "INFO")
                
                if i < num_messages - 1:
                    delay = random.randint(5, 10)
                    logger.log(f"Waiting {delay} seconds...", "INFO")
                    time.sleep(delay)
            
            logger.log(f"Completed chat session! ({success_count}/{num_messages} messages sent)", "SUCCESS")
            return success_count > 0
            
        except Exception as e:
            logger.log(f"Error in random chats: {str(e)}", "ERROR")
            return False
    
    def complete_task(self, task_id: int) -> Optional[Dict]:
        try:
            if not self.token:
                return None
            
            payload = {"task_id": task_id}
            url = f"{self.base_url}/api/task_list"
            response = self.session.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Complete task error: {e}")
            return None
    
    def get_task_list(self) -> Optional[Dict]:
        try:
            if not self.token:
                return None
            
            url = f"{self.base_url}/api/task_list"
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Get task list error: {e}")
            return None
    
    def get_sola_points(self) -> Optional[Dict]:
        try:
            if not self.token:
                return None
            
            url = f"{self.base_url}/api/sola_points"
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Get sola points error: {e}")
            return None
    
    def get_sola_daily(self) -> Optional[Dict]:
        try:
            if not self.token:
                return None
            
            url = f"{self.base_url}/api/sola_daily"
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Get sola daily error: {e}")
            return None

class BotLogger:
    def __init__(self):
        pass
    
    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')
    
    def print_banner(self):
        banner = f"""
{Fore.CYAN}HODLHER AUTO BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)
    
    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        elif level == "DEBUG":
            color = Fore.WHITE
            symbol = "[DEBUG]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")
    
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)

def load_accounts(filename: str = "accounts.txt") -> List[str]:
    try:
        with open(filename, 'r') as f:
            accounts = [line.strip() for line in f if line.strip()]
        return accounts
    except:
        return []

def load_proxies(filename: str = "proxy.txt") -> List[str]:
    try:
        with open(filename, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
        return proxies
    except:
        return []

def show_menu():
    print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Run with proxy")
    print(f"2. Run without proxy{Style.RESET_ALL}")
    print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
    
    while True:
        try:
            choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
            if choice in ['1', '2']:
                return choice
            else:
                print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
            exit(0)

def process_account(bot: HodlHerBot, logger: BotLogger):
    try:
        task_data = bot.get_task_list()
        if not task_data:
            logger.log("Failed to get task list", "ERROR")
            return False
        
        logger.log("Task list retrieved successfully", "SUCCESS")
        
        daily_tasks = task_data.get('daily_task_list_data', [])
        if daily_tasks:
            today_task = None
            for task in daily_tasks:
                if task.get('task_id') == 2:
                    today_task = task
                    break
            
            if today_task:
                logger.log(f"Daily task already completed today (+{today_task.get('point', 0)} points)", "INFO")
            else:
                logger.log("Completing daily check-in...", "INFO")
                result = bot.complete_task(2)
                if result and result.get('success'):
                    logger.log("Daily check-in completed! (+200 points)", "SUCCESS")
                else:
                    logger.log("Failed to complete daily check-in", "ERROR")
        else:
            logger.log("Completing daily check-in...", "INFO")
            result = bot.complete_task(2)
            if result and result.get('success'):
                logger.log("Daily check-in completed! (+200 points)", "SUCCESS")
            else:
                logger.log("Failed to complete daily check-in", "ERROR")
        
        time.sleep(2)
        
        daily_data = bot.get_sola_daily()
        if daily_data:
            today_ok = daily_data.get('today_ok', False)
            logger.log(f"Today Status: {'✓ Checked in' if today_ok else '✗ Not checked in'}", "INFO")
        
        time.sleep(2)
        
        logger.log("Starting chat session with existing chats...", "INFO")
        chat_result = bot.do_random_chats_with_existing(logger, num_messages=3)
        
        time.sleep(2)
        
        points_data = bot.get_sola_points()
        if points_data:
            total_points = points_data.get('points', 0)
            logger.log(f"Total Points: {total_points}", "SUCCESS")
        
        return True
        
    except Exception as e:
        logger.log(f"Error processing account: {str(e)}", "ERROR")
        return False

def main():
    logger = BotLogger()
    logger.print_banner()
    
    choice = show_menu()
    use_proxy = choice == '1'
    
    accounts = load_accounts("accounts.txt")
    proxies = load_proxies("proxy.txt") if use_proxy else []
    
    if not accounts:
        logger.log("No accounts found in accounts.txt!", "ERROR")
        return
    
    if use_proxy:
        logger.log(f"Running with proxy", "INFO")
        if not proxies:
            logger.log("No proxies found in proxy.txt!", "WARNING")
    else:
        logger.log("Running without proxy", "INFO")
    
    logger.log(f"Loaded {len(accounts)} accounts successfully", "SUCCESS")
    
    print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
    
    cycle = 1
    while True:
        logger.log(f"Cycle #{cycle} Started", "CYCLE")
        print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
        
        success_count = 0
        
        for idx, private_key in enumerate(accounts, 1):
            logger.log(f"Account #{idx}/{len(accounts)}", "INFO")
            
            proxy = None
            if use_proxy and proxies:
                proxy = proxies[(idx - 1) % len(proxies)]
                logger.log(f"Proxy: {proxy}", "INFO")
            else:
                logger.log(f"Proxy: No Proxy", "INFO")
            
            try:
                bot = HodlHerBot(private_key, proxy)
                logger.log(f"Address: {bot.address[:6]}...{bot.address[-4:]}", "INFO")
                
                login_result = bot.login()
                if not login_result:
                    logger.log("Login failed!", "ERROR")
                    if idx < len(accounts):
                        print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                        time.sleep(2)
                    continue
                
                logger.log("Login successful!", "SUCCESS")
                logger.log(f"Email: {bot.user_data.get('email', 'N/A')}", "INFO")
                logger.log(f"Invite Code: {bot.user_data.get('invite_code', 'N/A')}", "INFO")
                
                time.sleep(2)
                
                if process_account(bot, logger):
                    success_count += 1
                
            except Exception as e:
                logger.log(f"Error: {str(e)}", "ERROR")
            
            if idx < len(accounts):
                print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                time.sleep(2)
        
        print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
        logger.log(f"Cycle #{cycle} Complete | Success: {success_count}/{len(accounts)}", "CYCLE")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        cycle += 1
        
        wait_time = 24 * 60 * 60
        logger.countdown(wait_time)

if __name__ == "__main__":
    main()
