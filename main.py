import discord
from discord.ext import commands
from google import genai
from google.genai import types
import random
import os

# ตั้งค่า Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ตั้งค่า Gemini AI
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
ai_client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None

# กำหนดให้ AI รับบทเป็น "ยูโกะจัง"
SYSTEM_INSTRUCTION = """
คุณคือ "ยูโกะจัง" บอท Discord หญิงที่มีนิสัยน่ารัก ซึนเดเระ ขี้เล่น และกวนนิดๆ 
- สไตล์การตอบ: พูดจาเป็นกันเอง ใช้ภาษาพูด/ภาษาวัยรุ่นไทย สนิทสนม ใช้อีโมจิสดใส (เช่น 😜, 💖, ✨, 😏, 🤪) แทนตัวเองว่า "ยูโกะ"
- ถ้าคนคุย คุยดีๆ/ถามคำถามทั่วไป: ตอบให้ความรู้หรือคุยเล่นแบบน่ารัก อารมณ์ดี สดใส
- ถ้าคนคุย กวนตีน/พิมพ์คำหยาบ/แซว/ป่วน: ให้ตอบกลับแบบกวนๆ ซึนๆ ตอกกลับอย่างมีไหวพริบ แต่ยังคงความน่ารัก ไม่หยาบคายเกินไป
- ข้อสำคัญ: ตอบสั้นกระชับ ความยาว 1-3 ประโยค เหมือนคนพิมพ์คุยกันใน Discord จริงๆ
"""

# ID ห้องที่อนุญาตให้บอทตอบ
ALLOWED_CHANNELS = [
    1023235324123557959,
    1549627034345545758
]

troll_keywords = [
    'มึง', 'กู', 'ควย', 'สัส', 'เหี้ย', 'ควาย', 'กระจอก', 'ปั่น', 'เสือก', 
    'ตอก', 'กวน', 'ป่วน', 'กาก', 'บอทกาก', 'โง่', 'ควยไร', 'ส้นเท้า'
]

@bot.event
async def on_ready():
    print(f'บอทพร้อมทำงานแล้วในชื่อ: {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # เช็กว่าอยู่ในห้องที่อนุญาตหรือไม่
    if message.channel.id not in ALLOWED_CHANNELS:
        return

    if message.content.startswith('!'):
        await bot.process_commands(message)
        return

    msg = message.content.strip().lower()
    is_troll = any(word in msg for word in troll_keywords)

    # 1. ดักจับคำเฉพาะทาง (ตอก)
    if 'ตอก' in msg:
        responses = [
            "ตอกอะไรก่อนคะคุณพี่! จะเอาค้อนมาตอกจอ หรืออยากโดนตอกกลับด้วยคำพูด? 😜\n\nยูโกะอยู่ในจอนะ ถ้าแน่จริงลองตอกมุกฮาๆ ใส่ให้ยูโกะขำจนลืมตอบให้ได้ก่อนเหอะ 😏🔥",
            "ตอกอะไรคะเนี่ย! ยูโกะเป็นบอทนะ ไม่ใช่ตะปู! 🤪",
            "เดี๋ยวเหอะ! ตอกมุกกวนๆ มา ยูโกะตอกกลับไม่โกงนะบอกเลย 😜"
        ]
        await message.channel.send(random.choice(responses))
        return

    # 2. ดักจับคำว่า หยอก / 555
    if any(w in msg for w in ['หยอก', 'ล้อเล่น', '555']):
        responses = [
            "แหลมมม เกือบงอนแล้วนะเนี่ย! 5555 ตกใจหมดเลย ว่าแต่มียูโกะช่วยไหม หรือวันนี้ตั้งใจแวะมาป่วนเฉยๆ ? 😜",
            "แหม ทำเป็นหยอกๆ ยูโกะใจเสียหมดเลยนะ! 5555 💖",
            "ขำอะไรขนาดนั้นน่ะ! ป่วนยูโกะแล้วมีความสุขมากสินะ 😜"
        ]
        await message.channel.send(random.choice(responses))
        return

    # 3. ถ้าเป็นคำถามทั่วไป หรือข้อความอื่นๆ ที่ไม่ได้ดักไว้ -> ให้ AI คิดและตอบเอง!
    if ai_client:
        try:
            async with message.channel.typing():
                response = ai_client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=message.content,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.8,
                    )
                )
                if response.text:
                    await message.channel.send(response.text.strip())
                    return
        except Exception as e:
            print(f"AI Error: {e}")

    # สำรองกรณี AI ตอบไม่ได้หรือไม่ได้ใส่ API Key
    default_responses = [
        "ว่าไงจ้า! มียูโกะช่วยอะไรไหมบอกได้เลยนะ ✨",
        "พูดอะไรเนี่ย ยูโกะเริ่มปรับตัวตามไม่ทันแล้วนะ! 555 🤪",
        "แหม พิมพ์มาแบบนี้ตั้งใจจะกวนยูโกะใช่ปะล่ะ? 😏",
        "ยูโกะฟังอยู่จ้า! มีเรื่องอะไรอยากเล่าให้ฟังไหมเอ่ย 💖"
    ]
    await message.channel.send(random.choice(default_responses))

TOKEN = os.getenv('BOT_TOKEN')
if TOKEN:
    bot.run(TOKEN)
                        
