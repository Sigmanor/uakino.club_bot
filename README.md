<div align="center">

# uakino.club_bot 🎬

<h3>Readme Language</h3>

[![EN](https://img.shields.io/badge/English-0e7837.svg)](README.md) [![UA](https://img.shields.io/badge/Ukrainian-c9c9c9.svg)](README_UA.md)


A Telegram bot that provides random recommendations for movies, TV series, and cartoons from [uakino.me](https://uakino.me).

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

</div>

## 📖 Overview

This Telegram bot helps users discover new content by providing random recommendations for movies, TV series, and cartoons. It interfaces with uakino.me to offer a streamlined way to find your next watch through Telegram.

## ✨ Features

- 🎲 Random movie recommendations
- 📺 Random TV series suggestions
- 🎨 Random cartoon picks
- 🚀 Simple and intuitive commands
- 🐳 Docker support for easy deployment

> [!NOTE]
> When deploying in Docker, requests to the site may be blocked (error 403). It is recommended to run the bot locally to avoid this issue.

## 🛠️ Prerequisites

- Python 3.6 or higher
- Telegram Bot Token (get it from [@BotFather](https://t.me/botfather))
- Internet connection 😜

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sigmanor/uakino.club_bot.git
   cd uakino.club_bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env_example .env
   ```
   Edit `.env` and add your:
   - Telegram Bot Token
   - Your Telegram ID

## 🚀 Usage

### Run

```bash
python bot.py
```

## 🤖 Bot Commands

| Command    | Description                    |
|------------|--------------------------------|
| /start     | Get bot information           |
| /movie     | Get a random movie            |
| /serial    | Get a random TV series        |
| /cartoon   | Get a random cartoon          |

## 📝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🧪 Testing

Run the tests with:

```bash
python -m pytest __tests__
```

## 🤝 Support

If you encounter any problems or have suggestions, please [open an issue](https://github.com/Sigmanor/uakino.club_bot/issues).
