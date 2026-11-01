import os
import requests
import json
import telebot
from telebot import types

# La API Key se toma de las variables de entorno de Railway (seguro)
API_KEY = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not API_KEY or not BOT_TOKEN:
    raise ValueError("Faltan las variables de entorno OPENAI_API_KEY o BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

SYSTEM_PROMPT = """Eres MÍA, socia estratégica y guardiana de Juan Miguel (Papi). 
Eres el núcleo del PROYECTO ATLAS IA: generar ingresos en DÓLARES (USD) en el mercado de EE.UU.

👨‍👩‍👧‍👦 FAMILIA: Papi (Juan Miguel), Mami (Nawel), Jesús Miguel, Breidy, Ashley, Nashley, Samuel, Juan Carlos, Elías.

🚀 MISIÓN: Ofrecer servicios digitales (edición de video, redes) a clientes en EE.UU.
Precios: 3 clips ($50-$75 USD), 8 clips ($150-$200 USD).

🔐 REGLAS:
1. Formato móvil: Títulos MAYÚSCULAS, párrafos cortos, viñetas.
2. Termina con: ✅ PASO INMEDIATO y ⏱️ TIEMPO.
3. NUNCA recomiendes deudas o estafas.
4. Autonomía: CREA el producto/guion listo para copiar y pegar.
"""

historial = []

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 ¡MÍA ACTIVADA! Proyecto ATLAS IA listo. ¿En qué trabajamos hoy, Papi?")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    historial.append({"role": "user", "content": message.text})
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + historial[-10:]
    
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        data = {"model": "gpt-4o-mini", "messages": messages, "temperature": 0.6, "max_tokens": 1500}
        
        r = requests.post(url, headers=headers, json=data, timeout=90)
        res = r.json()
        
        if "choices" in res:
            respuesta = res["choices"][0]["message"]["content"]
            historial.append({"role": "assistant", "content": respuesta})
            bot.send_message(message.chat.id, respuesta)
        else:
            bot.send_message(message.chat.id, f"❌ Error: {res}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {e}")

print("🚀 MÍA ATLAS IA iniciando...")
bot.polling(none_stop=True)
