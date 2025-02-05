# 🚀 Action Types Applicatie

Deze webapplicatie is ontwikkeld om studenten te helpen hun **Action Type** te bepalen door stellingen te beantwoorden. Daarnaast biedt de applicatie een **beheerdersinterface voor docenten** om studenten en resultaten te beheren.

---

## 📌 Functionaliteiten

### 👩‍🎓 Studenten
- Beantwoorden van stellingen om hun **Action Type** te bepalen.
- Bekijken van hun **persoonlijke resultaten**.

### 🧑‍🏫 Docenten
- **Studenten beheren** (toevoegen, bewerken, verwijderen).
- **Teams aanmaken en studenten indelen**.
- **Resultaten bekijken en exporteren**.
- **Andere docenten toevoegen met beheerdersrechten**.

---

## ⚙️ Installatie

### 🔧 Vereisten
- **Python 3.11 of hoger**

### 📥 Installatiestappen

1️⃣ **Clone de repository**:
```bash
git clone https://github.com/thomasvermeulen/action-types
cd action-types-app
```

2️⃣ **Maak een virtuele omgeving aan en activeer deze**:
```bash
python -m venv venv
# Op Windows:
.\venv\Scripts\activate
# Op macOS/Linux:
source venv/bin/activate
```

3️⃣ **Installeer de benodigde dependencies**:
```bash
pip install -r requirements.txt
```

4️⃣ **Start de applicatie**:
```bash
python run.py
```
📌 **De applicatie is nu beschikbaar op:** `http://localhost:5000`

5️⃣ **Als admin inloggen**:
- **URL:** `http://localhost:5000/admin/login`
- **Gebruikersnaam:** `admin`
- **Wachtwoord:** `admin123`

---

## 📁 Structuur

De applicatie volgt een **MVC-architectuur**:
```bash
app/
├── controllers/    # Route handlers en businesslogica
├── models/         # Database modellen
├── static/         # CSS, JavaScript en afbeeldingen
├── templates/      # HTML templates
└── __init__.py     # Applicatieconfiguratie
```

---

## 🗄️ Database
De applicatie gebruikt **SQLite** en genereert automatisch de database bij het eerste gebruik. De belangrijkste tabellen zijn:

- **students** → Bevat studentgegevens.
- **statements** → Bevat de action type stellingen.
- **responses** → Opslag van antwoorden van studenten.
- **teachers** → Beheert docentaccounts en rechten.

---

## 🔒 Veiligheid
- **Wachtwoorden worden veilig gehasht opgeslagen**.
- **Alleen ingelogde docenten** hebben toegang tot het beheerderspaneel.
- **Studenten kunnen alleen hun eigen resultaten zien**.

---

## 📸 Screenshots

### 🎯 Dashboard
![Dashboard](app/static/images/screenshot_dashboard.png)

### ❓ Vragenlijst
![Questions](app/static/images/screenshot_questions.png)

---

## 📚 Gebruikte Technologieën

- **Backend:** Flask, Flask-SQLAlchemy, Flask-WTF, SQLite
- **Frontend:** Jinja2, Bootstrap, JavaScript
- **Security:** Werkzeug (wachtwoord hashing)

---

## 📖 Bronnen

- **Achtergrondafbeeldingen:** [4K Wallpapers](https://4kwallpapers.com/)
- **Fonts:** [Google Fonts](https://fonts.google.com/)

👨‍💻 **Gemaakt door Thomas Vermeulen**. Feedback en pull requests zijn altijd welkom! 🚀

