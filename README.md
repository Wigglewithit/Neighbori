# Neighbori

Neighbori is a lightweight, free-to-use platform built for connecting people through community-powered skill-sharing. 
Whether you want to learn something new, teach a skill, or offer services in exchange for knowledge, Neighbori enables all of that without the friction of traditional freelancing platforms.

##  Features

- User registration and profiles
- Skill listings and categories
- Requests for help or learning
- Skill exchanges or contributions
- Community feedback and ratings
- Admin dashboard for moderation

## Stack

- **Backend**: Django + PostgreSQL
- **Frontend**: HTML + Tailwind (planned)
- **Deployment**: To be hosted (Render, Railway, etc.)
- **License**: MIT

## Setup

1. Clone the repo  
   `git clone https://github.com/Wigglewithit/Neighbori.git`

2. Create a virtual environment  
   `python -m venv .venv`

3. Activate it  
   - On PowerShell: `.\.venv\Scripts\Activate.ps1`
   - On CMD: `.\.venv\Scripts\activate.bat`

4. Install dependencies  
   `pip install -r requirements.txt`

5. Run the server  
   `python manage.py runserver`

##  Folder Structure

```
Neighbori/
├── manage.py
├── main/
│   ├── migrations/
│   ├── templates/
│   ├── views.py
│   └── ...
├── .venv/
└── requirements.txt
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change or add.

##  License

This project is licensed under the MIT License.
