import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__, template_folder='../templates')

# Replace with your actual API Key or set as environment variable
# If using Gemini or DeepSeek, change the base_url accordingly
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# In-memory storage for chat history (per session in a real app)
chat_history = [
    {"role": "system", "content": "You are a professional Marketing and Business Strategy AI assistant for We-Wave-Agency. You provide data-driven insights, creative ad copy, and technical business solutions."}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    user_input = request.json.get("message")
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # 1. Add User Message to History
    chat_history.append({"role": "user", "content": user_input})

    try:
        # 2. Call the AI Model
        response = client.chat.completions.create(
            model="gpt-4o", # Or "gpt-3.5-turbo"
            messages=chat_history,
            temperature=0.7
        )

        ai_message = response.choices[0].message.content
        
        # 3. Add AI Response to History for memory
        chat_history.append({"role": "assistant", "content": ai_message})

        return jsonify({"response": ai_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset():
    global chat_history
    chat_history = [chat_history[0]] # Keep only the system prompt
    return jsonify({"status": "Chat reset successfully"})

if __name__ == "__main__":
    app.run(debug=True)
