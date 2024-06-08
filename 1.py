import discord
from discord.ext import commands
import google.generativeai as genai

# GenAI API anahtarını doğrudan buraya ekleyin
GEN_AI_API_KEY = "AIzaSyC79E_ENXjG7C6Fnn2U6_w_ca_lMVUn5Ng"  # API anahtarınızı buraya ekleyin

genai.configure(api_key=GEN_AI_API_KEY)

class TextBasedAssistant:
    def __init__(self):
        self.chat_session = None

    def start_chat_session(self):
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )
        self.chat_session = model.start_chat(history=[])

    def generate_ai_response(self, user_input):
        """Generates a response from the AI model."""
        response = self.chat_session.send_message(user_input)
        return response.text

# Discord botu ayarları
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
assistant = TextBasedAssistant()

TARGET_CHANNEL_ID = 1249089782521401455

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} olarak giriş yaptı!')
    assistant.start_chat_session()

@bot.event
async def on_message(message):
    if message.channel.id == TARGET_CHANNEL_ID:
        print(f'Mesaj alındı: {message.content}')
        if message.author != bot.user:
            if message.content.startswith('!sor'):
                question = message.content[len('!sor '):].strip()
                print(f'Soru alındı: {question}')

                try:
                    # AI yanıtı oluştur
                    response = assistant.generate_ai_response(question)
                    print(f'Aİ cevabı: {response}')

                    # Yanıtı hedef kanala gönder
                    await message.channel.send(response)
                except Exception as e:
                    print(f'Hata: {e}')
                    await message.channel.send("Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.")

TOKEN="MTI0ODg5ODI0NDAzODIzMDAyOA.GfuAfH.fWjkUCf7bZbyYLc1ORucLDVkkBQeYZbvwXqWZ0"  # Bot tokeninizi buraya ekleyin

if TOKEN:
    bot.run(TOKEN)
else:
    print("Bot token bulunamadı. Lütfen ortam değişkenini ayarlayın.")
