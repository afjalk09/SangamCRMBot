
from flask import Flask, render_template, request, jsonify
from agent import ask_crm

app = Flask(__name__)

# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# CHAT API
# ==========================================

@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    user_question = data.get("question")

    try:

        response = ask_crm(user_question)

        return jsonify({
            "success": True,
            "response": response
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "response": str(e)
        })


# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)

