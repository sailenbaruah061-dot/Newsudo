import asyncio
import time
import random
import json
import os
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatType, ChatMemberStatus
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

#=============== CONFIG ================
API_ID = 39035274 # Apna API ID daalein
API_HASH = "6a0b24e16c4bea2bbc975b7dbb0c1e64" # Apna API Hash daalein
BOT_TOKEN = "8931408596:AAHpQAeA0iLWLQjrltfJ1RZYfrh5HNrSbGQ" # Apna Bot Token daalein
OWNER_ID = 8722144519 # Apna Telegram ID daalein
BOT_USERNAME = "@ll_SUPRRME_XD_ll_BOT" # Apna bot username daalein

#=============== DUMMY SERVER FOR RENDER ================
class Handler(BaseHTTPRequestHandler):
def do_GET(self):
self.send_response(200)
self.end_headers()
self.wfile.write(b"Bot is running!")
def log_message(self, format, *args):
pass

def run_server():
port = int(os.environ.get("PORT", 10000))
server = HTTPServer(('0.0.0.0', port), Handler)
server.serve_forever()

Start server thread for Render
threading.Thread(target=run_server, daemon=True).start()

app = Client("fast_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

#Data storage
sudo_users = {OWNER_ID} # Owner is sudo by default
muted_users = set()
spam_active = False
spam_target = None
spam_count = 0
sticker_spam_active = False
custom_stickers = []

#Shayari storage
shayari_data = {
"love": [],
"sad": [],
"birthday": [],
"general": []
}

#Default shayari
default_shayari = {
"love": [
"❤️ प्यार में यूं मिलते हैं दिल,\nजैसे सागर में मिलती है नदी।\nतुमसे मिलकर लगता है,\nये दुनिया है सबसे हसीन! 💕",
"💝 तेरी एक मुस्कान,\nबदल देती है मेरी पहचान।\nतू है तो मैं हूं,\nतू नहीं तो कुछ नहीं! 🌹"
 ],
"sad": [
"🥀 टूटे दिल का दर्द,\nसमझता है कोई और।\nहंसते हुए चेहरे के पीछे,\nदेखता है कोई और! 😢",
"💔 अकेले बैठे हैं हम,\nतेरी यादों के सहारे।\nतू नहीं तो क्या हुआ,\nहै तेरी तस्वीर हमारे पास! 🥺"
 ],
"birthday": [
"🎂 जन्मदिन मुबारक हो आपको,\nहर खुशी हो आपके संग।\nखुशियां हों आपके पास इतनी,\nजितने आसमान में हैं बादल! 🎉",
"🎈 हर पल खुशियों से भरा हो,\nहर दिन नया उजियारा हो।\nआपका जीवन फूलों जैसा महके,\nहर सपना हकीकत में ढले! 🌟"
 ],
"general": [
"💫 जिंदगी एक सफर है,\nअलग-अलग रंग लिए।\nकभी हंसी तो कभी आंसू,\nकभी प्यार तो कभी गम लिए! 🌈",
"🌙 तन्हाई में अक्सर मिलता है सुकून,\nहवाओं में बसती हैं कहानियां।\nहर दर्द कहता है एक किस्सा,\nहर खुशी में छिपी होती है जवानियां! ⭐"
 ]
}

#Load saved data
def load_data():
global sudo_users, custom_stickers, shayari_data
try:
if os.path.exists("sudo_users.json"):
with open("sudo_users.json", "r") as f:
sudo_users = set(json.load(f))
if os.path.exists("custom_stickers.json"):
with open("custom_stickers.json", "r") as f:
custom_stickers = json.load(f)
if os.path.exists("shayari_data.json"):
with open("shayari_data.json", "r") as f:
shayari_data = json.load(f)
except Exception as e:
print(f"Error loading data: {e}")

def save_data():
with open("sudo_users.json", "w") as f:
json.dump(list(sudo_users), f)
with open("custom_stickers.json", "w") as f:
json.dump(custom_stickers, f)
with open("shayari_data.json", "w") as f:
json.dump(shayari_data, f)

Initialize default shayari
def init_shayari():
for category in default_shayari:
if not shayari_data.get(category):
shayari_data[category] = default_shayari[category]
save_data()

#=============== BUTTONS ================
def get_main_keyboard():
keyboard = InlineKeyboardMarkup([
[InlineKeyboardButton("➕ Add Me Baby", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
[InlineKeyboardButton("🏠 My Home", callback_data="home")],
[InlineKeyboardButton("👑 My Master", url=f"https://t.me/ll_SUPRRME_XD_ll")],
[InlineKeyboardButton("❓ Help", callback_data="help")],
[InlineKeyboardButton("⚡ Get Sudo", url=f"https://t.me/ll_SUPRRME_XD_ll")]
])
return keyboard

#=============== START COMMAND ================
@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
user = message.from_user
await message.reply_text(
f"🔥 Welcome {user.first_name}! 🔥\n\n"
f"I'm a powerful group management bot.\n\n"
f"Use buttons below to explore!",
reply_markup=get_main_keyboard()
)

#=============== BUTTON CALLBACK HANDLER ================
@app.on_callback_query()
async def button_callback(client, callback_query):
data = callback_query.data

if data == "help":
help_text = """
🤖 BOT COMMANDS 🤖

📊 Utility:
• .alive - Check bot status
• .ping - Check bot speed
• .speed - Bot response time

💬 Shayari:
• .love - Love shayari
• .sad - Sad shayari
• .shayari - General shayari
• .birthday - Birthday wishes
• .addshayari - Add shayari

⚡ Sudo Commands:
• .mute - Mute user globally
• .unmute - Unmute user
• .sticker - Sticker spam
• .stopraid - Stop sticker spam
• .spam - Spam user
• .stopspam - Stop spam

👑 Owner Only:
• .addsticker - Add sticker
• .addsudo - Add sudo user
• .removesudo - Remove sudo user
• .sudolist - List sudo users
• .mutelist - List muted users
"""
await callback_query.message.edit_text(
help_text,
reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back")]])
)

elif data == "back":
await callback_query.message.edit_text(
f"🔥 Welcome Back! 🔥\n\nUse buttons below to explore!",
reply_markup=get_main_keyboard()
)

elif data == "home":
await callback_query.message.edit_text(
f"🏠 My Home\n\n"
f"📊 Bot Stats:\n"
f"• Sudo Users: {len(sudo_users)}\n"
f"• Muted Users: {len(muted_users)}\n"
f"• Stickers: {len(custom_stickers)}\n"
f"• Status: Active 🟢\n\n"
f"👑 Owner:{OWNER_ID}",
reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back")]])
)

await callback_query.answer()

#Commands for everyone
@app.on_message(filters.command("alive", prefixes=[".", "/"]) & filters.group)

async def alive_command(client, message: Message):
await message.reply_text("✅ Bot is Online! 🚀")

@app.on_message(filters.command("ping", prefixes=[".", "/"]) & filters.group)

async def ping_command(client, message: Message):
start = time.time()
msg = await message.reply_text("🏓 Pinging...")
end = time.time()
ping_time = round((end - start) * 1000)
await msg.edit_text(f"🏓 Pong!\n⏱️ {ping_time}ms")

@app.on_message(filters.command("speed", prefixes=[".", "/"]) & filters.group)

async def speed_command(client, message: Message):
start = time.time()
msg = await message.reply_text("⚡ Checking speed...")
end = time.time()
response_time = round((end - start) * 1000)
await msg.edit_text(f"⚡ Bot Speed\n📡 Response Time: {response_time}ms\n🚀 Status: Super Fast!")

#Sudo-only commands
def is_sudo(user_id):
return user_id in sudo_users

@app.on_message(filters.command("mute", prefixes=[".", "/"]) & filters.group)

async def mute_command(client, message: Message):
if not is_sudo(message.from_user.id):
await message.reply_text("❌ Only sudo users can use this command!")
return

if not message.reply_to_message:
await message.reply_text("❌ Please reply to a user to mute them!")
return

target_user = message.reply_to_message.from_user
muted_users.add(target_user.id)
save_data()
await message.reply_text(f"✅ {mention} has been muted!")

@app.on_message(filters.command("unmute", prefixes=[".", "/"]) & filters.group)

async def unmute_command(client, message: Message):
if not is_sudo(message.from_user.id):
await message.reply_text("❌ Only sudo users can use this command!")
return

if not message.reply_to_message:
await message.reply_text("❌ Please reply to a user to unmute them!")
return

target_user = message.reply_to_message.from_user
if target_user.id in muted_users:
muted_users.remove(target_user.id)
save_data()
await message.reply_text(f"✅ {mention} has been unmuted!")
else:
await message.reply_text(f"❌ {target_user.first_name} is not muted!")

@app.on_message(filters.command("mutelist", prefixes=[".", "/"]) & filters.group)

async def mutelist_command(client, message: Message):
if not is_sudo(message.from_user.id):
await message.reply_text("❌ Only sudo users can use this command!")
return

if not muted_users:
await message.reply_text("📝 No users are muted currently!")
return

muted_list = "🔇 Muted Users List\n\n"
for user_id in muted_users:
try:
user = await client.get_users(user_id)
muted_list += f"• {user.first_name} ({user_id})\n"
except:
muted_list += f"• Unknown User ({user_id})\n"

await message.reply_text(muted_list)

#Sticker spam command
@app.on_message(filters.command("sticker", prefixes=[".", "/"]) & filters.group)

async def sticker_spam_command(client, message: Message):
if not is_sudo(message.from_user.id):
await message.reply_text("❌ Only sudo users can use this command!")
return

global sticker_spam_active

parts = message.text.split()
if len(parts) != 2:
await message.reply_text("❌ Usage: .sticker <count>\nExample: .sticker 50")
return

try:
count = int(parts[1])
if count > 100:
await message.reply_text("❌ Max limit is 100!")
return
except:
await message.reply_text("❌ Please provide a valid number!")
return

sticker_spam_active = True

if not custom_stickers:
await message.reply_text("❌ No stickers added yet!\nUse .addsticker to add stickers.")
return

for i in range(count):
if not sticker_spam_active:
break
sticker = random.choice(custom_stickers)
await message.reply_sticker(sticker)
await asyncio.sleep(0.1)

sticker_spam_active = False

@app.on_message(filters.command("stopraid", prefixes=[".", "/"]) & filters.group)

async def stop_raid_command(client, message: Message):
if not is_sudo(message.from_user.id):
await message.reply_text("❌ Only sudo users can use this command!")
return

global sticker_spam_active
sticker_spam_active = False
await message.reply_text("🛑 Sticker raid stopped!")

#Shayari commands
@app.on_message(filters.command("love"))
async def love_command(client, message: Message):
if shayari_data["love"]:
shayari = random.choice(shayari_data["love"])
await message.reply_text(f"💕 Love Shayari 💕\n\n{shayari}")

@app.on_message(filters.command("sad"))
async def sad_command(client, message: Message):
if shayari_data["sad"]:
shayari = random.choice(shayari_data["sad"])
await message.reply_text(f"🥀 Sad Shayari 🥀\n\n{shayari}")

@app.on_message(filters.command("shayari"))
async def general_shayari_command(client, message: Message):
if shayari_data["general"]:
shayari = random.choice(shayari_data["general"])
await message.reply_text(f"✨ Shayari ✨\n\n{shayari}")

@app.on_message(filters.command("birthday"))
async def birthday_command(client, message: Message):
if shayari_data["birthday"]:
shayari = random.choice(shayari_data["birthday"])
await message.reply_text(f"🎂 Birthday Shayari 🎂\n\n{shayari}")

@app.on_message(filters.command("addshayari"))
async def add_shayari_command(client, message: Message):
if not is_sudo(message.from_user.id):
await message.reply_text("❌ Only sudo users can add shayari!")
return

parts = message.text.split(" ", 2)
if len(parts) < 3:
await message.reply_text("❌ Usage: .addshayari <love/sad/birthday/general> <shayari>")
return

category = parts[1].lower()
shayari_text = parts[2]

if category in shayari_data:
shayari_data[category].append(shayari_text)
save_data()
await message.reply_text(f"✅ Shayari added to {category} category!")
else:
await message.reply_text("❌ Category must be: love, sad, birthday, or general")

#Spam tag command
@app.on_message(filters.command("spam", prefixes=[".", "/"]) & filters.group)

async def spam_command(client, message: Message):
if not is_sudo(message.from_user.id):
await message.reply_text("❌ Only sudo users can use this command!")
return

if not message.reply_to_message:
await message.reply_text("❌ Reply to a user and use: .spam <count> <message>")
return

parts = message.text.split(" ", 2)

if len(parts) < 3:
await message.reply_text("❌ Usage: .spam <count> <message>")
return

try:
count = int(parts[1])
if count > 100:
await message.reply_text("❌ Max limit is 100!")
return
except:
await message.reply_text("❌ Invalid number!")
return

target = message.reply_to_message.from_user
mention = target.mention
custom_text = parts[2]

for i in range(count):
await message.reply_text(f"{mention} {custom_text}")
await asyncio.sleep(0.1)

await message.reply_text(f"✅ Spam completed: {count} times!")


try:
count = int(parts[1])
if count > 100:
await message.reply_text("❌ Max spam count is 100!")
return
except:
await message.reply_text("❌ Please provide a valid number!")
return

target = message.reply_to_message.from_user
spam_target = target.id
spam_count = count
spam_active = True

for i in range(count):
if not spam_active:
break
await message.reply_text(f"{target.first_name}")
await asyncio.sleep(0.1)

spam_active = False
await message.reply_text(f"✅ Spammed {count} times!")

@app.on_message(filters.command("stopspam", prefixes=[".", "/"]) & filters.group)

async def stop_spam_command(client, message: Message):
if not is_sudo(message.from_user.id):
await message.reply_text("❌ Only sudo users can use this command!")
return

global spam_active
spam_active = False
await message.reply_text("🛑 Spam stopped!")

#Owner-only commands
@app.on_message(filters.command("addsticker", prefixes=[".", "/"]) & filters.group)

async def add_sticker_command(client, message: Message):
if message.from_user.id != OWNER_ID:
await message.reply_text("❌ Only owner can use this command!")
return

if not message.reply_to_message or not message.reply_to_message.sticker:
await message.reply_text("❌ Please reply to a sticker to add it!")
return

sticker_id = message.reply_to_message.sticker.file_id
custom_stickers.append(sticker_id)
save_data()
await message.reply_text(f"✅ Sticker added!\nTotal stickers: {len(custom_stickers)}")

@app.on_message(filters.command("addsudo", prefixes=[".", "/"]) & filters.group)

async def add_sudo_command(client, message: Message):
if message.from_user.id != OWNER_ID:
await message.reply_text("❌ Only owner can add sudo users!")
return

user_id = None

if message.reply_to_message:
user_id = message.reply_to_message.from_user.id
elif len(message.command) > 1:
try:
user_id = int(message.command[1])
except:
await message.reply_text("❌ Invalid user ID!")
return

if user_id:
sudo_users.add(user_id)
save_data()
user = await client.get_users(user_id)
await message.reply_text(f"✅ {user.first_name} added as sudo user!")
else:
await message.reply_text("❌ Reply to a user or provide user ID!")

@app.on_message(filters.command("removesudo", prefixes=[".", "/"]) & filters.group)

async def remove_sudo_command(client, message: Message):
if message.from_user.id != OWNER_ID:
await message.reply_text("❌ Only owner can remove sudo users!")
return

user_id = None

if message.reply_to_message:
user_id = message.reply_to_message.from_user.id
elif len(message.command) > 1:
try:
user_id = int(message.command[1])
except:
await message.reply_text("❌ Invalid user ID!")
return

if user_id and user_id in sudo_users and user_id != OWNER_ID:
sudo_users.remove(user_id)
save_data()
user = await client.get_users(user_id)
await message.reply_text(f"✅ {user.first_name} removed from sudo users!")
else:
await message.reply_text("❌ User not found in sudo list or cannot remove owner!")

@app.on_message(filters.command("sudolist", prefixes=[".", "/"]) & filters.group)

async def sudo_list_command(client, message: Message):
if not is_sudo(message.from_user.id):
await message.reply_text("❌ Only sudo users can use this command!")
return

if not sudo_users:
await message.reply_text("📝 No sudo users found!")
return

sudo_list = "👑 Sudo Users List\n\n"
for user_id in sudo_users:
try:
user = await client.get_users(user_id)
sudo_list += f"• {user.first_name}\n ┗ ID: {user_id}\n"
except:
sudo_list += f"• Unknown User\n ┗ ID: {user_id}\n"

await message.reply_text(sudo_list)

Message handler for logging and muting
@app.on_message(filters.group)
async def message_handler(client, message: Message):

try:
log_text = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
log_text += f"User: {message.from_user.first_name} [{message.from_user.id}] | "
log_text += f"Group: {message.chat.title} | "

if message.text:
log_text += f"Text: {message.text[:100]}"
elif message.sticker:
log_text += f"Sticker sent"

print(log_text)
except:
pass

# ✅ SAFE CHECK (ADD THIS BLOCK)
if not message.from_user:
return

user_id = message.from_user.id

# 🚫 OWNER & SUDO PROTECTION (IMPORTANT)
if user_id == OWNER_ID:
return

if user_id in sudo_users:
return

# ❌ ONLY MUTED USERS WILL BE DELETED
if user_id in muted_users:
try:
await message.delete()
except:
pass

# Log message
try:
log_text = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
log_text += f"User: {message.from_user.first_name} [{message.from_user.id}] | "
log_text += f"Group: {message.chat.title} | "
if message.text:
log_text += f"Text: {message.text[:100]}"
elif message.sticker:
log_text += f"Sticker sent"
print(log_text)
except:
pass

# Delete muted user messages
if message.from_user and message.from_user.id in muted_users:
try:
await message.delete()
print(f"Deleted message from muted user: {message.from_user.first_name}")
except:
pass

Start bot
def main():
load_data()
init_shayari()

# Add owner to sudo if not present
if OWNER_ID not in sudo_users:
sudo_users.add(OWNER_ID)
save_data()

print("🚀 Bot Started Successfully!")
print("✅ All features loaded!")
print("📝 Check logs for group messages")
print(f"👑 Owner ID: {OWNER_ID}")
print(f"📊 Sudo Users: {len(sudo_users)}")

app.run()

if name == "__main__":
main()

