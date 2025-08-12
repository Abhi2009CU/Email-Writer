#imports
import webbrowser
from threading import Timer
from flask import Flask, render_template, request
from together import Together
import os
from dotenv import load_dotenv

load_dotenv()


client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/right", methods=["POST"])
def right():
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
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[{"role": "user", "content": prompt}]
    )

    #Extract result from response
    result_text = response.choices[0].message.content

    #display ai result
    return render_template("reply.html", reply_text=result_text)

if __name__ == "__main__":
    Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(port=5000)