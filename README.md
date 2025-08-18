# Stranger Chat Application

A real-time chat application built with Django Channels and Flutter that allows users to chat with random strangers.

## Features

- Real-time messaging using WebSocket connections
- Anonymous chat with random strangers
- Automatic matchmaking system
- Modern UI with Flutter
- Message history and status indicators

## Backend Setup (Django)

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

The Django server will run on `http://localhost:8000`

## Frontend Setup (Flutter)

### Prerequisites
- Flutter SDK
- Android Studio / VS Code

### Installation

1. Navigate to your Flutter project directory
2. Install dependencies:
```bash
flutter pub get
```

3. Update the WebSocket URL in `main.dart`:
```dart
static const String WS_URL = 'ws://10.0.2.2:8000/ws/chat/';
```

4. Run the app:
```bash
flutter run
```

## How It Works

1. **Connection**: Users connect to the WebSocket endpoint
2. **Matchmaking**: The first user waits, the second user gets matched
3. **Chat**: Messages are sent between matched users
4. **Disconnection**: When a user disconnects, the other user is notified

## File Structure

```
├── backend/                 # Django backend
│   ├── settings.py         # Django settings
│   ├── urls.py             # URL configuration
│   └── asgi.py             # ASGI configuration
├── chat/                   # Chat app
│   ├── consumers.py        # WebSocket consumer
│   ├── models.py           # Database models
│   ├── routing.py          # WebSocket routing
│   └── views.py            # HTTP views
├── main.dart               # Flutter frontend
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**: Make sure the Django server is running and the URL in Flutter is correct
2. **Module Not Found**: Install missing dependencies with `pip install -r requirements.txt`
3. **Static Files Error**: Run `python manage.py collectstatic`

### Development Notes

- The backend uses in-memory channel layers for development
- For production, consider using Redis for channel layers
- The Flutter app is configured for Android emulator (10.0.2.2)
- For real devices, update the WebSocket URL to your server's IP address

## License

This project is for educational purposes.
