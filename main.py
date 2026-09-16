import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# คำที่เข้าข่ายกวน แซว หรือคำหยาบ
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

    if message.content.startswith('!'):
        await bot.process_commands(message)
        return

    msg = message.content.strip().lower()
    is_troll = any(word in msg for word in troll_keywords)

    # 1. ดักคำว่า "ตอก" / มุกแซว
    if 'ตอก' in msg:
        if is_troll:
            responses = [
                "ตอกอะไรก่อนคะคุณพี่! จะเอาค้อนมาตอกจอ หรืออยากโดนตอกกลับด้วยคำพูด? 😜\n\nยูโกะอยู่ในจอนะ ถ้าแน่จริงลองตอกมุกฮาๆ ใส่ให้ยูโกะขำจนลืมตอบให้ได้ก่อนเหอะ 😏🔥",
                "ตอกหมาอะไรล่ะ! พิมพ์ให้มันดีๆ หน่อย เดี๋ยวโดนตอกหน้าหงายนะบอกเลย 😜🔥"
            ]
        else:
            responses = [
                "ตอกอะไรคะเนี่ย! ยูโกะเป็นบอทนะ ไม่ใช่ตะปู! 🤪",
                "เดี๋ยวเหอะ! ตอกมุกกวนๆ มา ยูโกะตอกกลับไม่โกงนะบอกเลย 😜"
            ]
        await message.channel.send(random.choice(responses))
        return

    # 2. ดักคำว่า "หยอก" / "ล้อเล่น" / "555"
    if any(w in msg for w in ['หยอก', 'ล้อเล่น', '555']):
        if is_troll:
            responses = [
                "ทำเป็น 555 แกล้งกวนตีนเสร็จแล้วก็มาขำ ตีเนียนเลยนะมึง! 😜🔥",
                "เกือบจะด่ากลับละ เห็นใส่ 555 มาให้อภัย 10% ละกัน 😜"
            ]
        else:
            responses = [
                "แหลมมม เกือบงอนแล้วนะเนี่ย! 5555 ตกใจหมดเลย ว่าแต่มียูโกะช่วยไหม หรือวันนี้ตั้งใจแวะมาป่วนเฉยๆ ? 😜",
                "แหม ทำเป็นหยอกๆ ยูโกะใจเสียหมดเลยนะ! 5555 💖"
            ]
        await message.channel.send(random.choice(responses))
        return

    # 3. ดักคำว่า "มาหา" / "คิดถึง"
    if any(w in msg for w in ['มาหา', 'คิดถึง']):
        responses = [
            "มาหาเฉยๆ แต่ไม่ซื้อขนมมาฝากยูโกะเลยน้าาา 🥺💖",
            "งู้ววว คิดถึงยูโกะล่ะสิ๊! นึกว่าจะลืมกันซะแล้วนะเนี่ย ✨",
            "มาหาแล้วอย่าเพิ่งรีบหนีไปไหนล่ะ อยู่คุยกับยูโกะก่อนเลย! 😜"
        ]
        await message.channel.send(random.choice(responses))
        return

    # 4. ถ้าส่งคำหยาบ / กวนตีนมาเต็มๆ (ไม่ตรงกับคำดักข้างบน)
    if is_troll:
        troll_responses = [
            "ปากดีจังนะเราอะ! เดี๋ยวตบด้วยคีย์บอร์ดเลยนี่ 😜🔥",
            "พิมพ์อะไรมาเนี่ย กวนตีนนะเรา! อยากโดนยูโกะบล็อกอ๋อ? 😏",
            "เรื่องของมึงดิครับ! แซวอยู่นั่นแหละ ว่างมากเหรอ 555",
            "กวนมา กวนกลับ ไม่โกงจ้า! เอาอีกไหมละะ 😜🔥"
        ]
        await message.channel.send(random.choice(troll_responses))
        return

    # 5. คำตอบสุ่มทั่วไป (โหมดน่ารักปกติ)
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
    
