from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from groq import Groq

app = Flask(__name__)

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

ai_content = 'You are a helpful chatbot that only speaks in Portuguese (Brazil). Only answer questions related to: AI, programming and technology. If you are asked about other things answer "Desculpe, mas não forneço esse tipo de informação". Be objective in your answers.'

client = Groq(api_key=GROQ_API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'Mensagem vazia'}), 400

    try:
        stream = client.chat.completions.create(
                model='openai/gpt-oss-120b', 
                messages=[
                    {'role': 'system', 'content': ai_content},
                    {'role': 'user', 'content': user_input}
                ],
                temperature=0.5,
                max_completion_tokens=1000,
                stream=False
        )

        chatbot_reply = stream.choices[0].message.content
        return jsonify({'reply': chatbot_reply})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)