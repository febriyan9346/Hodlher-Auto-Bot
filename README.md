# Hodlher Auto Bot

[![Register](https://img.shields.io/badge/Register-HodlHer-blue)](https://dapp.hodlher.ai/register?code=HDLCMH73TH)

🔗 **Register Link:** [https://dapp.hodlher.ai/register?code=HDLCMH73TH](https://dapp.hodlher.ai/register?code=HDLCMH73TH)

---

## 📋 Description

Automated bot for HodlHer DApp that handles:
- 🔐 Auto login with wallet signature
- ✅ Daily check-in tasks
- 💬 Automated chat interactions
- 🎯 Point tracking
- 🔄 24-hour cycle automation
- 🌐 Proxy support

## ✨ Features

- **Multi-Account Support**: Run multiple accounts simultaneously
- **Proxy Integration**: Optional proxy support for enhanced privacy
- **Auto Daily Check-in**: Automatically completes daily tasks (+200 points)
- **Smart Chat System**: Random chat interactions with existing conversations
- **Real-time Logging**: Detailed colored logs with timestamps (WIB timezone)
- **Error Handling**: Robust error management and retry mechanisms
- **24h Cycle**: Automatic daily cycles with countdown timer

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Clone Repository

```bash
git clone https://github.com/febriyan9346/Hodlher-Auto-Bot.git
cd Hodlher-Auto-Bot
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## 📝 Configuration

### 1. Prepare Account File

Create `accounts.txt` in the root directory with your private keys (one per line):

```
0xYourPrivateKey1
0xYourPrivateKey2
0xYourPrivateKey3
```

⚠️ **Warning**: Keep your private keys secure! Never share them publicly.

### 2. Prepare Proxy File (Optional)

Create `proxy.txt` in the root directory (one proxy per line):

```
http://user:pass@host:port
http://host:port
socks5://user:pass@host:port
```

## 🎮 Usage

### Run the Bot

```bash
python bot.py
```

### Select Mode

When prompted, choose:
1. **Run with proxy** - Uses proxies from `proxy.txt`
2. **Run without proxy** - Direct connection

### Bot Flow

1. Login to each account
2. Complete daily check-in task
3. Perform random chat interactions (3 messages)
4. Display total points
5. Wait 24 hours before next cycle

## 📊 File Structure

```
Hodlher-Auto-Bot/
├── bot.py              # Main bot script
├── accounts.txt        # Private keys (create this)
├── proxy.txt           # Proxy list (optional)
├── requirements.txt    # Python dependencies
└── README.md          # Documentation
```

## 📦 Dependencies

```
web3>=6.0.0
eth-account>=0.9.0
requests>=2.31.0
colorama>=0.4.6
pytz>=2023.3
```

## 🔧 Configuration Details

### Chat Messages

The bot uses predefined chat messages for natural interactions:
- Greetings
- Casual conversations
- Interest-based questions
- Personal topics

Messages are randomly selected and sent with 5-10 second intervals.

### Task IDs

- **Task ID 2**: Daily check-in (+200 points)

## 📈 Features Breakdown

### Login System
- Web3 wallet signature authentication
- Automatic token management
- Session persistence

### Task Management
- Automatic daily check-in
- Task completion verification
- Point tracking

### Chat System
- Uses existing chat conversations
- Random message selection
- Natural conversation flow
- Streaming response handling

### Logging System
- Color-coded messages
- WIB timezone timestamps
- Multiple log levels (INFO, SUCCESS, ERROR, WARNING, DEBUG)
- Progress tracking

## ⚠️ Important Notes

1. **First Chat Creation**: Before running the bot, manually create at least one chat on the HodlHer DApp
2. **Private Key Security**: Never commit your `accounts.txt` file to version control
3. **Rate Limiting**: The bot includes delays to prevent rate limiting
4. **Network**: Configured for INJEVM network

## 🛡️ Security Recommendations

- ✅ Use dedicated wallets for bot activities
- ✅ Keep private keys in secure storage
- ✅ Add `accounts.txt` and `proxy.txt` to `.gitignore`
- ✅ Use proxies for enhanced privacy
- ✅ Regularly monitor bot activities

## 🐛 Troubleshooting

### Common Issues

**"No existing chats found"**
- Solution: Manually create a chat on the HodlHer DApp first

**"Login failed"**
- Check private key format
- Verify network connection
- Try with/without proxy

**"Connection timeout"**
- Check internet connection
- Verify proxy settings
- Try increasing timeout values

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/febriyan9346/Hodlher-Auto-Bot/issues)
- **Telegram**: Contact @febriyan9346 (if available)

## 📄 License

This project is for educational purposes only. Use at your own risk.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## ⭐ Star History

If this bot helps you, please consider giving it a star! ⭐

---

**Disclaimer**: This bot is for educational purposes. Always comply with HodlHer's Terms of Service. The developer is not responsible for any misuse or violations.

Made with ❤️ by FEBRIYAN
