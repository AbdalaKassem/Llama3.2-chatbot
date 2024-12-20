from huggingface_hub import InferenceClient

# Hugging Face API Client
client = InferenceClient(api_key="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")

def get_response(chat_history):
    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.2-3B-Instruct",
        messages=chat_history,
        max_tokens=500
    )
    return completion.choices[0].message.content

def generate_title(chat_history):
    prompt = f"Generate a concise and informative title for this chat: {chat_history}"
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.2-3B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )
    return response.choices[0].message.content.strip()
