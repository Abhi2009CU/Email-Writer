# Imports
import webbrowser
from threading import Timer
from flask import Flask, redirect, render_template, request
from together import Together
import os
from dotenv import load_dotenv
from plyer import notification

# Load environment variables
load_dotenv(dotenv_path=".env")

# Initialize Flask app and Together client
app = Flask(__name__)
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

# Function to edit the .env file with new settings
def editEnv(path, keys:dict):
    with open(path, "w") as file:
        file.writelines(f"{key}={value}\n" for key, value in keys.items())

# Function to check settings and validate API key and model
def checkSettings(api_key, model_name, port):
    temp_client = Together(api_key=api_key)
    try:
        response = temp_client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=1  # Keep request tiny
        )
        
        editEnv(".env", {"TOGETHER_API_KEY": api_key, "MODEL_NAME": model_name, "PORT": port})
        notification.notify(
            title='Email-Writer',
            message='Model verified successfully and API key is valid.',
            timeout=5
        )
        return True
    except Exception as e:
        notification.notify(
                title='Email-Writer',
                message='Failed to verify model or authenticate API key. Please verify your inputs.',
                timeout=5
            )
        return False

# Route to handle settings configuration
@app.route("/settings", methods=["GET", "POST"])
def config():
    api_key = request.form.get("api_key", "")
    model = request.form.get("model", "")
    port = request.form.get("port", "")
    if api_key and model and port:
        if (checkSettings(api_key, model, port)):
            load_dotenv(dotenv_path=".env", override=True)
            global client
            client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
            return redirect("/")
        return render_template("settings.html", error="Invalid API key and/or model name. Please try again.")
    else:
        return render_template("settings.html", error="Please fill in all fields.")

# Route to handle the main page
@app.route("/", methods=["GET", "POST"])
def index():
    if not (os.getenv("TOGETHER_API_KEY") and os.getenv("MODEL_NAME") and os.getenv("PORT")):
        return redirect("/settings")
    return render_template("index.html")

# Route to handle writing tasks
@app.route("/write", methods=["POST"])
def write():
    #Get form data
    content = request.form.get("content", "")
    choice = request.form.get("choice", "")

    #Prepare prompt based on choice
    if choice == "1":
        prompt = f"Generate a reply based on this email content:\n{content}"
    elif choice == "2":
        prompt = f"Generate a new email based on this prompt:\n{content}"
    else:
        prompt = f"Other task with content:\n{content}"

    #Contact ai and receive response
    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"),
        messages=[{"role": "user", "content": prompt}]
    )

    #Extract result from response
    result_text = response.choices[0].message.content

    #display ai result
    return render_template("reply.html", reply_text=result_text)

# Main entry point to run the Flask app
if __name__ == "__main__":
    url = f"http://127.0.0.1:{os.getenv('PORT', 5000)}"
    Timer(1, lambda: webbrowser.open(url)).start()
    app.run(port=os.getenv("PORT", 5000))