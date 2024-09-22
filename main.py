import os, requests, time, crayons

def print_banner():
    print(crayons.blue('██     ██ ██ ███    ██ ███████ ███    ██ ██ ██████  '))
    print(crayons.blue('██     ██ ██ ████   ██ ██      ████   ██ ██ ██   ██ '))
    print(crayons.blue('██  █  ██ ██ ██ ██  ██ ███████ ██ ██  ██ ██ ██████  '))
    print(crayons.blue('██ ███ ██ ██ ██  ██ ██      ██ ██  ██ ██ ██ ██      '))
    print(crayons.blue(' ███ ███  ██ ██   ████ ███████ ██   ████ ██ ██      '))
    print()
    print("Join our Telegram channel: https://t.me/winsnip")



class MoonBix:
    def __init__(self, token, proxy=None):
        self.session = requests.session()
        self.session.headers.update({
            'authority': 'www.binance.info',
            'accept': '*/*',
            'accept-language': 'en-EG,en;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'clienttype': 'web',
            'content-type': 'application/json',
            'lang': 'en',
            'origin': 'https://www.binance.info',
            'referer': 'https://www.binance.info/en/game/tg/moon-bix',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        })
        
        if proxy:
            self.session.proxies.update({'http': proxy, 'https': proxy})

        self.token = token
        self.game_response = None

    def login(self):
        try:
            response = self.session.post(
                'https://www.binance.info/bapi/growth/v1/friendly/growth-paas/third-party/access/accessToken',
                json={'queryString': self.token, 'socialType': 'telegram'},
            )
            if response.status_code == 200:
                self.session.headers['x-growth-token'] = response.json()['data']['accessToken']
                return True
            return False
        except Exception as e: 
            print(crayons.red(f"Error during login: {e}")) 

    def user_info(self):
        try:
            response = self.session.post(
                'https://www.binance.info/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/user/user-info',
                json={'resourceId': 2056},
            )
            return response.json()
        
        except Exception as e: 
            print(crayons.red(f"Error during get info: {e}")) 

    def game_data(self):
        try:
            while True:
                response = requests.post('https://vemid42929.pythonanywhere.com/api/v1/moonbix/play', json=self.game_response).json()
                if response['message'] == 'success' and response['game']['log'] >= 100:
                    self.game = response['game']
                    return True
        except Exception as e: 
            print(crayons.red(f"Error get gamedata: {e}")) 

    def complete_game(self):
        try:
            response = self.session.post(
                'https://www.binance.info/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/game/complete',
                json={'resourceId': 2056, 'payload': self.game['payload'], 'log': self.game['log']},
            )
            return response.json()['success']
        except Exception as e: 
            print(crayons.red(f"Error during complete game: {e}")) 

    def start_game(self):
        try:
            while True:
                response = self.session.post(
                    'https://www.binance.info/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/game/start',
                    json={'resourceId': 2056},
                )
                self.game_response = response.json()
                if self.game_response['code'] == '000000':
                    return True
                elif self.game_response['code'] == '116002':
                    print(crayons.red('Attempts not enough! Switching to the next account.'))
                    return False
                print(crayons.red("ERROR! Cannot start game."))
                return False
            
        except Exception as e: 
            print(crayons.red(f"Error during start game: {e}")) 

    def start(self):
        if not self.login():
            print(crayons.red("Failed to login"))
            return
        print(crayons.green("Logged in successfully!"))
        if not self.user_info():
            print(crayons.red("Failed to get Userdata"))
            return
        while self.start_game():
            print(crayons.cyan("Game has started!"))

            if not self.game_data():
                print(crayons.red("Failed to generate game data!"))
                return
            print(crayons.green("Game data generated successfully!"))

            sleep(45)

            if not self.complete_game():
                print(crayons.red("Failed to complete game"))

            print(crayons.yellow(f"Game completed! You earned + {self.game['log']}"))
            sleep(15)

def sleep(seconds):
    while seconds > 0:
        time_str = time.strftime('%H:%M:%S', time.gmtime(seconds))
        time.sleep(1)
        seconds -= 1
        print(f'\rWaiting {time_str}', end='', flush=True)
        
    print()

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    proxies = [line.strip() for line in open('proxy.txt') if line.strip()]  
    print(crayons.yellow("============================= Starting =============================="))
    while True:
        tokens = [line.strip() for line in open('data.txt')]
        for index, token in enumerate(tokens, start=1):
            print(crayons.magenta(f'============================= Account {index} ============================='))
            proxy = proxies[(index - 1) % len(proxies)] if proxies else None
            x = MoonBix(token, proxy)
            x.start()
            print(crayons.magenta(f'============================= Account {index} Done ========================'))
            sleep(15)

        print(crayons.green("All accounts have been completed"))
        sleep(3600)
