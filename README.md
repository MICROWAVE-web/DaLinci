Here’s the translated version of the text:

---

# DaLinci.com - Link Shortener with Analytics Tracking

DaLinci.com is a Django application for shortening links with the ability to track statistics and generate QR codes. The application supports user registration via two methods: email or phone number. Users can also create personalized shortened links and view their usage statistics.

## Key Features

- **Link shortening:** Generation of unique short links for long URLs.
- **Analytics tracking:** View the statistics of clicks for each link.
- **User registration:**
  - Via email.
  - By phone number (with a confirmation code sent).
- **QR codes:** Generate QR codes for each shortened link.
- **User-friendly interface:** Modern design with responsive layout.
- **Link management:** Delete or view detailed information about created links.

## Technologies

- **Backend:** Django 4
- **Frontend:** Jinja2
- **Database:** SQLite (can be replaced with any Django-supported database, such as PostgreSQL)
- **Email sending:** Yandex SMTP
- **Authentication:**
  - Custom user model with login via email or phone.
  - SMS code implementation for phone number confirmation.

## Installation

### Step 1: Clone the repository
```bash
git clone https://github.com/your-repository/DaLinci.git
cd DaLinci
```

### Step 2: Set up the virtual environment
```bash
python -m venv venv
source venv/bin/activate # For Linux/MacOS
venv\Scripts\activate    # For Windows
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure the `.env` file
Create a `.env` file in the root of the project and specify the settings, for example:
```env
SECRET_KEY=your_secret_key
DEBUG=True


# SMTP settings (for sending email)
EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@yandex.ru
EMAIL_HOST_PASSWORD=your_password
EMAIL_USE_TLS=True
```

### Step 5: Apply migrations
```bash
python manage.py migrate
```

### Step 6: Create a superuser
```bash
python manage.py createsuperuser
```

### Step 7: Run the development server
```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to start using the application.

## Main Pages

- **Home page:** A field for entering a URL and generating a short link.
- **Link list:** A list of all created links with their statistical information.
- **Statistics:** Detailed information on the number of clicks for each link.
- **Login:** Registration and login via email or phone number.

## Screenshots

### Home Page
![Снимок экрана 2025-01-04 135256](https://github.com/user-attachments/assets/fe183e8e-3c8c-46d3-9ceb-b251a45b4b3f)

### Link List
![Снимок экрана 2025-01-04 140046](https://github.com/user-attachments/assets/29b950df-6c36-498a-97a2-d901f0c229a4)

### Link details
![Снимок экрана 2025-01-04 140204](https://github.com/user-attachments/assets/1678eebe-fd67-4eda-a156-bcb55ca58ccf)

## Future Improvements

- Support for integration with other SMS services.
- Addition of an API for link shortening.
- Enhanced analytics: geolocation, user device, etc.

---

Developed with ❤️

### What is included in the `README.md`:

1. **Project description.**
2. **Installation instructions:**
   - Cloning the repository.
   - Setting up the virtual environment.
   - Installing dependencies.
   - Configuring settings.
3. **Feature description.**
4. **Screenshots:** Images you provided are included.
5. **Future improvements:** Development plan.

