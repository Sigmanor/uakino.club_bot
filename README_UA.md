# uakino.club_bot 🎬

[![EN](https://img.shields.io/badge/Language-English-red.svg)](README.md) [![UA](https://img.shields.io/badge/Language-Ukrainian-yellow.svg)](README_UA.md)

Телеграм-бот, який надає випадкові рекомендації фільмів, серіалів та мультфільмів з сайту [uakino.me](https://uakino.me).

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## 📖 Огляд

Цей Телеграм-бот допомагає відкривати новий контент, надаючи випадкові рекомендації фільмів, серіалів та мультфільмів.

## ✨ Особливості

- 🎲 Випадкові рекомендації фільмів
- 📺 Випадкові рекомендації серіалів
- 🎨 Випадковий рекомендації мультфільмів
- 🚀 Прості та інтуїтивно зрозумілі команди
- 🐳 Підтримка Docker для легкого розгортання

## 🛠️ Вимоги для розгортання

- Python 3.6 або вище
- Токен Telegram бота (отримайте його від [@BotFather](https://t.me/botfather))
- Підключення до Інтернету 😜

## 📦 Встановлення

1. **Клонуйте репозиторій**
   ```bash
   git clone https://github.com/Sigmanor/uakino.club_bot.git
   cd uakino.club_bot
   ```

2. **Встановіть залежності**
   ```bash
   pip install -r requirements.txt
   ```

3. **Налаштуйте середовище**
   ```bash
   cp .env_example .env
   ```
   Відредагуйте `.env` та додайте:
   - Токен Telegram бота
   - Ваш Telegram ID

## 🚀 Використання

### Стандартний запуск

```bash
python bot.py
```

### Docker

```bash
docker build -t uakino.club_bot .
docker run -d --name uakino-bot uakino.club_bot
```

### Docker Compose

```bash
docker compose up -d
```

## 🤖 Команди бота

| Команда   | Опис                           |
|-----------|--------------------------------|
| /start    | Отримати інформацію про бота   |
| /movie    | Отримати випадковий фільм      |
| /serial   | Отримати випадковий серіал     |
| /cartoon  | Отримати випадковий мультфільм |

## 📝 Внесок

1. Зробіть форк репозиторію
2. Створіть гілку для вашої функції (`git checkout -b feature/amazing-feature`)
3. Зробіть коміт ваших змін (`git commit -m 'Add amazing feature'`)
4. Відправте зміни у гілку (`git push origin feature/amazing-feature`)
5. Відкрийте Pull Request

## 🧪 Тестування

Запустіть тести за допомогою:

```bash
python -m pytest __tests__
```

## 🤝 Підтримка

Якщо ви зіткнулися з проблемами або маєте пропозиції, будь ласка, [створіть issue](https://github.com/Sigmanor/uakino.club_bot/issues).