
# Email-Writer

Email-Writer is a Flask-based web application that leverages the Together AI API to help you generate and reply to emails effortlessly. Whether you want to draft a new email or respond to an existing one, this tool uses advanced AI models to assist you in writing effective email content quickly.

---

## Features

- **Generate email replies** based on the content you provide.
- **Create new emails** from simple prompts.
- Easy-to-use web interface powered by Flask.
- Dynamic configuration of API key, AI model, and server port.
- Real-time AI response generation using Together API.
- Desktop notifications for success and error alerts (via plyer).

---

## Getting Started

### Prerequisites

- Python 3.8+
- Virtual environment tool (recommended)
- Together API key (sign up at [Together](https://together.ai/))

### Installation

1. Clone the repository:

```bash
git clone https://github.com/Abhi2009CU/Email-Writer.git
cd Email-Writer
```
2. Create and activate a virtual environment:

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```
or 
```bash
pip install together plyer flask python-dotenv
```

### Running the App

```bash
python main.py
```

This will start the Flask server and automatically open your default browser at `http://127.0.0.1:<PORT>`.

---

## Usage

* Visit the `/settings` page to configure your API key, model name, and port. The app saves these settings automatically to a `.env` file in the project root and loads them on startup.
* Use the main interface to input email content and select whether to generate a reply or create a new email.
* Submit the form to receive AI-generated email content.

---

## Technologies Used

* [Flask](https://flask.palletsprojects.com/)
* [Together API](https://www.together.ai/)
* [Plyer](https://plyer.readthedocs.io/en/latest/)
* [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## License

This project is licensed under the MIT License.

---
