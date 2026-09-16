import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

troll_words = ['มึง', 'กู', 'ควย', 'ส้นเท้า', 'เหี้ย', 'สัส', 'ควาย', 'กระจอก', 'ปั่น', 'เสือก']

@bot.event
async def on_ready():
    print(f'บอทพร้อมทำงานแล้วในชื่อ: {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!'):
        await bot.process_commands(message)
        return

    msg = message.content.strip().lower()
    is_troll = any(word in msg for word in troll_words)

    if 'สบายดีไหม' in msg or 'สบายดีมั้ย' in msg:
        if is_troll:
            responses = ['สบายดีว่ะ และมึงล่ะ', 'ก็สบายดี ไม่ได้ตายง่ายๆ หรอกมึง', 'สบายดีดิ แล้วมึงเป็นไรมากป่ะเนี่ย']
        else:
            responses = ['สบายดีครับ แล้วเราล่ะ?', 'เรื่อยๆ ครับผม ขอบคุณที่ถามนะ']
        await message.channel.send(random.choice(responses))
        return

    if msg.startswith('ไง') or 'ไง' in msg:
        if is_troll:
            responses = ['ไงมึง มีไรป่ะเนี่ย', 'ไงวัยรุ่น มีไรให้กูช่วย', 'ไงเอ็ด มีไรว่ามา']
        else:
            responses = ['ไงครับสบายดีไหม', 'ไงครับ มีอะไรให้ช่วยไหม', 'สวัสดีครับผม']
        await message.channel.send(random.choice(responses))
        return

    if 'ทำไรอยู่' in msg:
        if is_troll:
            responses = ['นั่งตอบแชทมึงอยู่นี่ไง', 'เรื่องของกูดิ', 'เฝ้าดิสอยู่ มึงอ่ะว่างมากอ๋อ']
        else:
            responses = ['กำลังเฝ้าเซิร์ฟเวอร์อยู่ครับ', 'ตอบแชทเพื่อนๆ อยู่ครับผม']
        await message.channel.send(random.choice(responses))
        return

    if is_troll:
        troll_responses = [
            "มึงเป็นไรมากป่ะเนี่ย?",
            "พูดคนเดียวก็เป็นเนาะกู",
            "ถามจริง รกแชทว่ะ",
            "กวนตีนมา กวนตีนกลับ ไม่โกงครับ",
            "เรื่องของมึงดิครับ!"
        ]
        await message.channel.send(random.choice(troll_responses))
        return

    default_responses = ["รับทราบครับ", "โอเคครับผม", "ครับผม"]
    await message.channel.send(random.choice(default_responses))

TOKEN = os.getenv('BOT_TOKEN')
if TOKEN:
    bot.run(TOKEN)
  
