💬 ChatTiko – Real-Time Chat Application

A modern Real-Time Chat Application built using Django, Django Channels (WebSocket), PostgreSQL, and Tailwind CSS.

This project supports real-time one-to-one and group messaging with a clean and responsive UI.

🚀 Tech Stack
🔹 Backend

Django

Django Channels

PostgreSQL

Redis

ASGI (Daphne)

🔹 Frontend

Tailwind CSS

HTML5

JavaScript (WebSocket API)

✨ Features

🔐 User Registration & Login

👤 Profile with Photo Upload

💬 One-to-One Chat

👥 Group Chat

⚡ Real-Time Messaging using WebSocket

🟢 Online/Offline Status

📱 Responsive Modern UI

🗂️ Chat History Stored in Database

📁 Project Structure
chat_project/
│── chat/                # Chat application
│── users/               # Authentication & Profile
│── static/              # CSS, JS, Images
│── templates/           # HTML files
│── chat_project/        # Main project settings
│── manage.py
│── requirements.txt
⚙️ Installation Guide
1️⃣ Clone the Repository
git clone https://github.com/your-username/chat-tiko.git
cd chat-tiko
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Setup PostgreSQL Database

Create a PostgreSQL database and update settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'chat_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
5️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate
6️⃣ Create Superuser
python manage.py createsuperuser
7️⃣ Run Redis Server

Make sure Redis is running:

redis-server
8️⃣ Run Development Server (ASGI)
daphne chat_project.asgi:application

OR

python manage.py runserver
🔌 WebSocket Configuration

settings.py must include:

ASGI_APPLICATION = "chat_project.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}