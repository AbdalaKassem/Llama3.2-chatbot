from flask import Flask, request, render_template, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import uuid
from model_interaction import get_response, generate_title

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chats.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "your_secret_key"  # Required for Flask session
db = SQLAlchemy(app)

# Database Models
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    messages = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(36), nullable=False)  # Associate chats with a user

# Initialize database
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    # Assign a unique ID to new users
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())  # Generate a unique user ID
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_id = session.get("user_id")
    chat_id = request.json.get("chat_id")
    user_message = request.json.get("message", "")

    # Retrieve the chat only if it belongs to the current user
    chat = Chat.query.filter_by(id=chat_id, user_id=user_id).first() if chat_id else None

    # Construct chat history
    chat_history = []
    if chat:
        chat_history = eval(chat.messages)
    chat_history.append({"role": "user", "content": user_message})

    # Get response from model
    response = get_response(chat_history)
    chat_history.append({"role": "assistant", "content": response})

    # Save chat in the database
    if not chat:
        # New chat
        title = generate_title(chat_history).strip('"')
        new_chat = Chat(title=title, messages=str(chat_history), user_id=user_id)
        db.session.add(new_chat)
        db.session.commit()
        chat_id = new_chat.id
    else:
        # Update existing chat
        chat.messages = str(chat_history)
        db.session.commit()

    return jsonify({"response": response, "chat_id": chat_id, "title": chat.title if chat else title})

@app.route("/chats", methods=["GET"])
def get_chats():
    user_id = session.get("user_id")
    chats = Chat.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": chat.id, "title": chat.title} for chat in chats])

@app.route("/chat/<int:chat_id>", methods=["GET"])
def get_chat(chat_id):
    user_id = session.get("user_id")
    chat = Chat.query.filter_by(id=chat_id, user_id=user_id).first_or_404()
    return jsonify({"id": chat.id, "title": chat.title, "messages": eval(chat.messages)})

@app.route("/new-chat", methods=["POST"])
def new_chat():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    # Create a new chat with an empty message history
    title = "New Chat"
    new_chat = Chat(title=title, messages="[]", user_id=user_id)
    # db.session.add(new_chat)
    # db.session.commit()
    
    return jsonify({"id": new_chat.id, "title": new_chat.title})

# @app.route("/new-chat", methods=["POST"])
# def new_chat():
#     # Create a new chat with an empty message history
#     title = "New Chat"
#     new_chat = Chat(title=title, messages="[]")
#     # db.session.add(new_chat)
#     # db.session.commit()
#     return jsonify({"id": new_chat.id, "title": new_chat.title})

if __name__ == "__main__":
    app.run(debug=True)
