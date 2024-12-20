# Llama 3.2 Chatbot

This project is an interface for the Llama 3.2 3B Instruct model. It allows users to interact with the model through a web-based chat interface.

## Features

- **Chat Interface**: A simple and intuitive chat interface to interact with the Llama model.
- **Session Persistence**: Chats are session-resistant, meaning they are stored in the session and will be available as long as the session is active.
- **Dynamic Chat List**: View and select from a list of previous chats.
- **New Chat Creation**: Start new chats with a single click.
- **Message Sending**: Send messages and receive responses from the Llama model.

## How It Works

1. **Setup**: The project uses Flask for the backend and SQLite for storing chat data.
2. **Chat Storage**: Chats are stored in the database and associated with a unique user ID stored in the session.
3. **Session Management**: When the browser is closed, the session data is deleted, and all chat data is lost.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/AbdalaKassem/Llama3.2-chatbot.git
   cd Llama3.2-chatbot
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   flask run
   ```

## Usage

1. Open your browser and navigate to `http://127.0.0.1:5000/`.
2. Start a new chat by clicking the "New Chat" button.
3. Type your message in the input box and click "Send".
4. View and select previous chats from the chat list.

## Important Note

- **Session Persistence**: The chats are session-resistant, meaning they are stored in the session and will be available as long as the session is active. However, when you close the browser, all data gets deleted.

## File Structure

```
Llama3.2-chatbot/
├── app.py
├── model_interaction.py
├── requirements.txt
├── static/
│   └── style.css
├── templates/
│   └── index.html
└── README.md
```

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Hugging Face](https://huggingface.co/) for providing the Llama model.
- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [SQLite](https://www.sqlite.org/index.html) for the database.

Feel free to contribute to this project by submitting issues or pull requests.
