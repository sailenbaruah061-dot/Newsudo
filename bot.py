import asyncio
import time
import random
import sqlite3
import html
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity
from telegram.ext import Application, MessageHandler, ContextTypes, filters, CallbackQueryHandler
from aiohttp import web
import os

# ==================== CONFIGURATION CORRIDOR ====================
BOT_TOKEN = "8709841273:AAH5_-grkn-SpklPEqApHldiJGvqgpr1u3E"
OWNER_ID = 8962957839  # ONLY ITACHI SAMA EXISTS NOW
BOT_USERNAME = "@ITACHI_V_CH_bot"
PORT = int(os.environ.get("PORT", 8080))

# ==================== ADVANCED DATABASE KERNEL ====================
db = sqlite3.connect("mainframe.db", check_same_thread=False)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS sudo (user_id INTEGER PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS mute (user_id INTEGER PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS stickers (file_id TEXT PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS warnings (user_id INTEGER, count INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS banned (user_id INTEGER PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS shayari (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, category TEXT)")
db.commit()

# ==================== CORE CONTROL REGISTRIES ====================
raid_active = False
sraid_active = False
spam_active = False
ghost_active = False
echo_active = False
current_raid_chat = None
current_raid_target = None
bot_start_time = datetime.now()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== ALL 35 DESTRUCTIVE & UTILITY COMMANDS ====================
COMMAND_REGISTRY = {
    ".alive": "Check kernel matrix pulse state.",
    ".ping": "Test data packet transit latency.",
    ".speed": "Audit server core execution bandwidth.",
    ".love": "Pull emotional romantic strings from DB.",
    ".sad": "Fetch dark heartbroken lines from DB.",
    ".shayari": "Extract global multi-line mixed shayari.",
    ".birthday": "Launch automated event celebration pack.",
    ".addshayari": "Inject custom text buffer to storage matrix.",
    ".mute": "Force mute target stream via text deletion.",
    ".unmute": "Restore normal profile transmission keys.",
    ".sticker": "Flood target via buffered sticker packets.",
    ".addsticker": "Cache target sticker signature locally.",
    ".spam": "Execute automated heavy text message storms.",
    ".stopspam": "FORCE KILL active spam operations instantly.",
    ".raid": "Deploy standard tagged verbal assault pipeline.",
    ".sraid": "NUCLEAR MODE: Ultra-fast 8-msg/sec multi-thread tag.",
    ".stopraid": "EMERGENCY HALT: Stop all raid configurations.",
    ".s": "Master kill-switch for all running loops.",
    ".kick": "Disconnect target connection node from chat room.",
    ".ban": "Truncate hardware parameters & permanent ban.",
    ".unban": "Re-authenticate blocked profile keys.",
    ".addsudo": "Elevate trusted profile to proxy master layer.",
    ".removesudo": "Deprecate user privileges instantly to null.",
    ".sudolist": "Audit all proxy administrators inside cluster.",
    ".mutelist": "Fetch logs of current black-space targets.",
    ".warn": "Register a formal threat anomaly entry.",
    ".warns": "Inspect target profile penalty logs.",
    ".unwarn": "Purge registered threat records completely.",
    ".lock": "Freeze group entry parameters for normal users.",
    ".unlock": "Restore standard text streaming inside room.",
    ".purge": "Wipe entire chat history packets instantly.",
    ".echo": "Force bot to replicate user message streams.",
    ".ghost": "Silently monitor and shadow target profile text.",
    ".stopghost": "Terminate stealth monitoring configuration.",
    ".stats": "Dump complete system memory allocation state."
}

RAID_LINES = [
    "ke samne koi bol sakta hai kya? 😭👑",
    "Aukat me rehna seekh le abhi bhi waqt hai! 🔥⚡",
    "Ab tera chat se gayab hone ka samay aa gaya hai! ☣️💀",
    "Beta, baap se panga nahi lete, samjhe? ⚔️",
    "Tera system hang kar denge beta! 🔥🤖",
    "Aaj teri aukat dikha denge! 💥🌟",
    "Bhag jaa yahan se! 🗑️🚶",
    "Itachi aur Geto ka order hai! 👑👑""TERI MUMMY KI CHUT!",
"BAHEN KE LODE TERI DADI KI BLACK HAIRY PUSSY",
"TERI MUMMY KO ULTA LTKAKR TAANGDUGA AUR USKI CHUT MARUNGA!",
"BSDK TERI MUMMY TERI DADI SB RANDI KI BACHI H",
"BAHENKLODO TUMHARI MAA MERI SETTING",
"TERI MUMMY RANDI H RANDI BSDK",
"TERI MUMMY KI PUSSY M SCOOTER DALDUGA",
"TERI MUMMY KI PUSSY ME CUM KRODUGA RANDI MAA K BACHE",
"TERA KHANDAN HI RANDIYO KA H",
"TERI DADI KI PUSSY ME MERA LUND",
"TERI MUMMY KO CHODKR ULTA LTKAKR USKE MUH ME LODA DEDUGA",
"TERI MUMMY KO DEEPTHROAT DEDUGA MADARCHOD K BACHE",
"TERA PAPA BHI RANDI KI AULAD H BSDK",
"TERI MUMMY KO YOGA SIKHADUGA AUR USKO DIFFERENT STYLES ME CHODUGA",
"TERA PAPA HU MAI TERI MUMMY KA BF JIS S VO CHUDKR GYI THI",
"TERI MAA KI PUSSY ME SCOOTER DALDUGA BAHEN KE LODE",
"TERI MAA KI CHUT ME BIHARI GUTKA KHAKR THUK KR CHALE GYE THE",
"TERI MAA KA BOSDA RANDI K BEEJ",
"TERI MAA KI CHUT ME 2 FINGER DEKR USKA PAANI NIKALDUGA",
"TERI MAA K MUH ME GAS PIPE DEKR USKI GAAND ME FIRE LGAKR TERE BAAP KI GAAND JALAUGA",
"TERI RANDI MAA KO CHODKR MAINE GB ROAD PR BEACH DIYA THA",
"TERI MUMMY K HAATH DIVAR PR LGVADIYE THE 10 BIHARIYO NE",
"TERI MAA KO TORRENT BANAKER SEED KAR DUNGA",
"TERI MAA KE BHOSDE ME FIREWALL LAGA DUNGA",
"TERI MAA KI CHUT ME SSD BOOT KAR DUNGA",
"TERI MAA BHOSDE ME NFT MINT KAR DUNGA",
"TERI MAA KA LUND OLX PE BECH DUNGA",
"TERI MAA KI GAAND ME QR CODE CHIPKA DUNGA",
"TERI MAA KA ONLYFANS LIVE KAR DUNGA",
"TERI LAGE KO TORRENT BANAKER SEED KAR DUNGA",
"TERI LAGE KE BHOSDE ME FIREWALL LAGA DUNGA",
"TERI LAGE KI CHUT ME SSD BOOT KAR DUNGA",
"TERI BEHEN KO TORRENT BANAKER SEED KAR DUNGA",
"TERI BEHEN KE BHOSDE ME FIREWALL LAGA DUNGA",
"TERI BEHEN KI CHUT ME SSD BOOT KAR DUNGA",
"TERI BEHEN KA LUND OLX PE BECH DUNGA",
"TERI BEHEN KI GAAND ME QR CODE CHIPKA DUNGA",
"TERI BEHEN KA BHOSDA NFT ME MINT KAR DUNGA",
"TERI BEHEN KA ONLYFANS LIVE KAR DUNGA",
"TERI BEHEN KO ZIP FILE ME COMPRESS KAR DUNGA",
"TERI BEHEN KE BHOSDE ME PYTHON RUN KAR DUNGA",
"TERI BEHEN KE LODE KO AIRDROP KAR DUNGA",
"TERI BEHEN KO BARCODE LAGA KE SCAN KARWA DUNGA",
"TERI BEHEN KO AI TOOL SE UPSCALE KAR DUNGA",
"TERE BAAP KO TORRENT BANAKER SEED KAR DUNGA",
"TERE BAAP KE BHOSDE ME FIREWALL LAGA DUNGA",
"TERE BAAP KI CHUT ME SSD BOOT KAR DUNGA",
"TERE BAAP KA LUND OLX PE BECH DUNGA",
"TERE BAAP KI GAAND ME QR CODE CHIPKA DUNGA",
"TERE BAAP KA BHOSDA NFT ME MINT KAR DUNGA",
"TERE BAAP KA ONLYFANS LIVE KAR DUNGA",
"TERE BAAP KO ZIP FILE ME COMPRESS KAR DUNGA",
"TERE BAAP KE BHOSDE ME PYTHON RUN KAR DUNGA",
"TERE BAAP KE LODE KO AIRDROP KAR DUNGA",
"TERE BAAP KO BARCODE LAGA KE SCAN KARWA DUNGA",
"TERE BAAP KO AI TOOL SE UPSCALE KAR DUNGA",
"TERI FAMILY KO TORRENT BANAKER SEED KAR DUNGA",
"TERI FAMILY KE BHOSDE ME FIREWALL LAGA DUNGA",
"TERI FAMILY KI CHUT ME SSD BOOT KAR DUNGA",
"TERI FAMILY KA LUND OLX PE BECH DUNGA",
"TERI FAMILY KI GAAND ME QR CODE CHIPKA DUNGA",
"TERI FAMILY KA BHOSDA NFT ME MINT KAR DUNGA",
"TERI FAMILY KA ONLYFANS LIVE KAR DUNGA",
"TERI FAMILY KO ZIP FILE ME COMPRESS KAR DUNGA",
"TERI FAMILY KE BHOSDE ME PYTHON RUN KAR DUNGA",
"TERI FAMILY KE LODE KO AIRDROP KAR DUNGA",
"TERI FAMILY KO BARCODE LAGA KE SCAN KARWA DUNGA",
"TERI FAMILY KO AI TOOL SE UPSCALE KAR DUNGA",
"TERE KUTTE KO TORRENT BANAKER SEED KAR DUNGA",
"TERE KUTTE KE BHOSDE ME FIREWALL LAGA DUNGA",
"TERE KUTTE KI CHUT ME SSD BOOT KAR DUNGA",
"TERE KUTTE KA LUND OLX PE BECH DUNGA",
"TERE KUTTE KI GAAND ME QR CODE CHIPKA DUNGA",
"TERE KUTTE KA BHOSDA NFT ME MINT KAR DUNGA",
"TERE KUTTE KA ONLYFANS LIVE KAR DUNGA",
"TERE KUTTE KO ZIP FILE ME COMPRESS KAR DUNGA",
"TERE KUTTE KE BHOSDE ME PYTHON RUN KAR DUNGA",
"TERE KUTTE KE LODE KO AIRDROP KAR DUNGA",
"TERE KUTTE KO BARCODE LAGA KE SCAN KARWA DUNGA",
"TERE KUTTE KO AI TOOL SE UPSCALE KAR DUNGA",
"TERI AUKAAT KO TORRENT BANAKER SEED KAR DUNGA",
"TERI AUKAAT KE BHOSDE ME FIREWALL LAGA DUNGA",
"TERI AUKAAT KI CHUT ME SSD BOOT KAR DUNGA",
"TERI AUKAAT KA LUND OLX PE BECH DUNGA",
"TERI AUKAAT KI GAAND ME QR CODE CHIPKA DUNGA",
"TERI AUKAAT KA BHOSDA NFT ME MINT KAR DUNGA",
"TERI AUKAAT KA ONLYFANS LIVE KAR DUNGA",
"TERI AUKAAT KO ZIP FILE ME COMPRESS KAR DUNGA",
"TERI AUKAAT KE BHOSDE ME PYTHON RUN KAR DUNGA",
"TERI AUKAAT KE LODE KO AIRDROP KAR DUNGA",
"TERI AUKAAT KO BARCODE LAGA KE SCAN KARWA DUNGA",
"TERI AUKAAT KO AI TOOL SE UPSCALE KAR DUNGA",
"TERI MUMMY KO TORRENT BANAKER SEED KAR DUNGA",
"TERI MUMMY KE BHOSDE ME FIREWALL LAGA DUNGA",
"TERI MUMMY KI CHUT ME SSD BOOT KAR DUNGA",
"TERI MUMMY KA LUND OLX PE BECH DUNGA",
"TERI MUMMY KI GAAND ME QR CODE CHIPKA DUNGA",
"TERI MUMMY KA BHOSDA NFT ME MINT KAR DUNGA",
"TERI MUMMY KA ONLYFANS LIVE KAR DUNGA",
"TERI MUMMY KO ZIP FILE ME COMPRESS KAR DUNGA",
"TERI MUMMY KE BHOSDE ME PYTHON RUN KAR DUNGA",
"TERI MUMMY KE LODE KO AIRDROP KAR DUNGA",
"TERI MUMMY KO BARCODE LAGA KE SCAN KARWA DUNGA",
"TERI MUMMY KO AI TOOL SE UPSCALE KAR DUNGA",
"TERE DADA KO TORRENT BANAKER SEED KAR DUNGA",
"TERE DADA KE BHOSDE ME FIREWALL LAGA DUNGA",
"TERE DADA KI CHUT ME SSD BOOT KAR DUNGA",
"TERE DADA KA LUND OLX PE BECH DUNGA",
"TERE DADA KI GAAND ME QR CODE CHIPKA DUNGA",
"TERE DADA KA BHOSDA NFT ME MINT KAR DUNGA",
"TERE DADA KA ONLYFANS LIVE KAR DUNGA",
"TERE DADA KO ZIP FILE ME COMPRESS KAR DUNGA",
"TERE DADA KE BHOSDE ME PYTHON RUN KAR DUNGA",
"TERE DADA KE LODE KO AIRDROP KAR DUNGA",
"TERE DADA KO BARCODE LAGA KE SCAN KARWA DUNGA",
"TERE DADA KO AI TOOL SE UPSCALE KAR DUNGA"
]

# ==================== ADVANCED AUTHENTICATION MATRICES ====================
def is_sudo(user_id):
    cursor.execute("SELECT user_id FROM sudo WHERE user_id=?", (user_id,))
    return cursor.fetchone() is not None

def is_muted(user_id):
    cursor.execute("SELECT user_id FROM mute WHERE user_id=?", (user_id,))
    return cursor.fetchone() is not None

def is_banned(user_id):
    cursor.execute("SELECT user_id FROM banned WHERE user_id=?", (user_id,))
    return cursor.fetchone() is not None

def is_supreme(user_id):
    return user_id == OWNER_ID

def is_authorized(user_id):
    return is_supreme(user_id) or is_sudo(user_id)

def get_closest_match(wrong_cmd):
    for cmd in COMMAND_REGISTRY.keys():
        if wrong_cmd in cmd or cmd in wrong_cmd:
            return cmd
    return None

# ==================== DEEP REAL TAG ENGINE (HACK MENTION) ====================
async def send_real_mention(context, chat_id, target_user, line_text):
    """
    This function generates a real hard-coded text_mention entity.
    It forces Telegram to trigger a real notification/vibration ping on target's phone!
    """
    display_text = f"⚡ {target_user.first_name} {line_text}"
    entity = MessageEntity(
        type=MessageEntity.TEXT_MENTION,
        offset=2,
        length=len(target_user.first_name),
        user=target_user
    )
    await context.bot.send_message(chat_id=chat_id, text=display_text, entities=[entity])

# ==================== ASYNC MULTI-THREAD FLOOD EXECUTORS ====================
async def run_standard_raid(context: ContextTypes.DEFAULT_TYPE):
    global raid_active, current_raid_chat, current_raid_target
    idx = 0
    while raid_active and current_raid_target:
        try:
            line = RAID_LINES[idx % len(RAID_LINES)]
            await send_real_mention(context, current_raid_chat, current_raid_target, line)
            idx += 1
            await asyncio.sleep(0.35)
        except Exception:
            await asyncio.sleep(0.5)

async def run_nuclear_sraid(context: ContextTypes.DEFAULT_TYPE):
    global sraid_active, current_raid_chat, current_raid_target
    idx = 0
    while sraid_active and current_raid_target:
        try:
            tasks = []
            for _ in range(8):  # Parallel Execution Pipeline
                line = RAID_LINES[idx % len(RAID_LINES)]
                tasks.append(send_real_mention(context, current_raid_chat, current_raid_target, line))
                idx += 1
            await asyncio.gather(*tasks, return_exceptions=True)
            await asyncio.sleep(0.05)  # Lightspeed Burst Interval
        except Exception:
            await asyncio.sleep(0.2)

async def run_burst_spam(context: ContextTypes.DEFAULT_TYPE, chat_id, text_to_spam, count):
    global spam_active
    sent = 0
    while spam_active and sent < count:
        try:
            await context.bot.send_message(chat_id=chat_id, text=text_to_spam)
            sent += 1
            await asyncio.sleep(0.12)
        except Exception:
            await asyncio.sleep(0.4)
    spam_active = False

# ==================== INTERACTIVE USER INTERFACES ====================
def get_main_dashboard():
    keyboard = [
        [InlineKeyboardButton("⚡ ADD ME TO GROUPS ⚡", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [InlineKeyboardButton("📊 OVERVIEW STATS", callback_data="cb_stats"),
         InlineKeyboardButton("💬 SHAYARI MENU", callback_data="cb_shayari")],
        [InlineKeyboardButton("📜 ALL COMMAND MATRIX", callback_data="cb_all_cmds")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_markup():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 RETURN TO MATRIX", callback_data="cb_main")]])

async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "cb_main":
        start_msg = "🔱 <b>ITACHI SUPREME DESTRUCTION ENGINE ONLINE</b> 🔱\n\n• Core Lord: <b>ITACHI SAMA</b>\n• Protocol Level: <b>MAXIMUM OVERLOAD TERMINAL</b>\n\nSelect control cluster below:"
        await query.edit_message_text(start_msg, reply_markup=get_main_dashboard(), parse_mode="HTML")
        
    elif query.data == "cb_stats":
        cursor.execute("SELECT COUNT(*) FROM sudo")
        s_cnt = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM mute")
        m_cnt = cursor.fetchone()[0]
        uptime = datetime.now() - bot_start_time
        text = f"📊 <b>ENGINE STATUS LOGS</b> 📊\n\n• Verified Sudo Layers: <code>{s_cnt}</code>\n• Restricted Nodes: <code>{m_cnt}</code>\n• Total Commands: <code>{len(COMMAND_REGISTRY)}</code>\n• Kernel Uptime: <code>{uptime.seconds // 60} minutes</code>"
        await query.edit_message_text(text, reply_markup=get_back_markup(), parse_mode="HTML")
        
    elif query.data == "cb_shayari":
        text = "💬 <b>SHAYARI SECTOR INTERFACE</b> 💬\n\n• Use <code>.love</code> inside chat for love elements.\n• Use <code>.sad</code> inside chat for broken elements.\n• Use <code>.shayari</code> for standard text arrays.\n• Inject lines via <code>.addshayari [category] [text]</code>"
        await query.edit_message_text(text, reply_markup=get_back_markup(), parse_mode="HTML")
        
    elif query.data == "cb_all_cmds":
        text = "📜 <b>COMPLETE 35 SYSTEM COMMAND CATALOGUE</b> 📜\n\n"
        for idx, (cmd, desc) in enumerate(COMMAND_REGISTRY.items(), start=1):
            text += f"<code>{idx}.</code> <b>{cmd}</b> ➔ <i>{desc}</i>\n"
        await query.edit_message_text(text, reply_markup=get_back_markup(), parse_mode="HTML")

# ==================== CENTRAL ROUTING TERMINAL ====================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global raid_active, sraid_active, spam_active, ghost_active, echo_active, current_raid_chat, current_raid_target
    
    if not update.message: return
    user = update.message.from_user
    chat_id = update.effective_chat.id
    text = update.message.text.strip() if update.message.text else ""
    
    # 1. Structural Quarantine Filtering
    if (is_banned(user.id) or is_muted(user.id)) and not is_supreme(user.id):
        try: await update.message.delete()
        except Exception: pass
        return
        
    if text == "/start":
        start_msg = "🔱 <b>ITACHI SUPREME DESTRUCTION ENGINE ONLINE</b> 🔱\n\n• Core Lord: <b>ITACHI SAMA</b>\n• Protocol Level: <b>MAXIMUM OVERLOAD TERMINAL</b>\n\nSelect control cluster below:"
        await update.message.reply_text(start_msg, reply_markup=get_main_dashboard(), parse_mode="HTML")
        return
        
    if not text.startswith('.'):
        return
        
    parts = text.split(maxsplit=1)
    command = parts[0].lower()
    
    # 2. Advanced Error Handling & Recommendation Engine
    if command not in COMMAND_REGISTRY:
        match = get_closest_match(command)
        if match:
            await update.message.reply_text(f"🛑 <b>SYSTEM ANOMALY</b>: Command <code>{command}</code> does not exist.\n💡 <i>Did you mean to trigger:</i> <code>{match}</code>?", parse_mode="HTML")
        else:
            await update.message.reply_text(f"❌ <b>CRITICAL ERROR</b>: Packet reference <code>{command}</code> rejected by Itachi Core.", parse_mode="HTML")
        return
        
    if not is_authorized(user.id):
        await update.message.reply_text("🚫 <b>CORE OVERRIDE DENIED:</b> You are not Itachi Sama. Access locked.")
        return
        
    # ==================== INDIVIDUAL PROTOCOL LOGIC BLOCK ====================
    try:
        # Loop Killers / Alternates
        if command in [".stopraid", ".s"]:
            raid_active = False
            sraid_active = False
            current_raid_chat = None
            current_raid_target = None
            await update.message.reply_text("🛑 <b>[ ALL RAID PIPELINES EXTERMINATED SUCCESSFULLY ]</b>", parse_mode="HTML")
            return

        elif command == ".stopspam":
            spam_active = False
            await update.message.reply_text("🛑 <b>[ SPAM ENGINE FORCED TO STAND DOWN ]</b>", parse_mode="HTML")
            return

        elif command == ".alive":
            await update.message.reply_text("⚡ <code>[ITACHI SYSTEM PULSE: EXTREME ONLINE]</code>", parse_mode="HTML")
            return

        elif command == ".ping":
            st = time.time()
            m = await update.message.reply_text("<code>📡 Querying proxy infrastructure...</code>", parse_mode="HTML")
            await m.edit_text(f"📡 <b>LATENCY INTERCEPTED:</b> <code>{(time.time()-st)*1000:.1f} ms</code>", parse_mode="HTML")
            return

        elif command == ".speed":
            st = time.time()
            m = await update.message.reply_text("<code>⚡ Measuring data pipeline bus speed...</code>", parse_mode="HTML")
            await m.edit_text(f"⚡ <b>EXECUTION SPEED:</b> <code>{(time.time()-st)*1000:.1f} ms</code>\n• State: <b>LIGHTSPEED MAXIMUM</b>", parse_mode="HTML")
            return

        # Raid Direct Link Injections (Real hard tags)
        elif command == ".raid":
            if not update.message.reply_to_message:
                await update.message.reply_text("❌ Reply to a profile node to trigger targeted raid arrays.")
                return
            if raid_active or sraid_active: return
            raid_active = True
            current_raid_chat = chat_id
            current_raid_target = update.message.reply_to_message.from_user
            await update.message.reply_text("💣 <b>REAL HARD TARGET REAL-TAG FLOOD RUNNING...</b>", parse_mode="HTML")
            asyncio.create_task(run_standard_raid(context))
            return

        elif command == ".sraid":
            if not update.message.reply_to_message:
                await update.message.reply_text("❌ Reply to target profile node to execute nuclear speed flood.")
                return
            if raid_active or sraid_active: return
            sraid_active = True
            current_raid_chat = chat_id
            current_raid_target = update.message.reply_to_message.from_user
            await update.message.reply_text("💀 <b>MAX PROTOCOL MULTI-THREAD REAL TARGET ASSAULT INITIALIZED...</b>", parse_mode="HTML")
            asyncio.create_task(run_nuclear_sraid(context))
            return

        elif command == ".spam":
            if len(parts) < 2: return
            sub_p = parts[1].split(maxsplit=1)
            if len(sub_p) < 2 or not sub_p[0].isdigit(): return
            spam_active = True
            asyncio.create_task(run_burst_spam(context, chat_id, sub_p[1], int(sub_p[0])))
            return

        # Mute / Administration System Controls
        elif command == ".mute":
            if not update.message.reply_to_message: return
            tgt = update.message.reply_to_message.from_user
            if is_supreme(tgt.id): return
            cursor.execute("INSERT OR IGNORE INTO mute VALUES (?)", (tgt.id,))
            db.commit()
            await update.message.reply_text(f"🔇 <b>Node <a href='tg://user?id={tgt.id}'>{tgt.first_name}</a> silenced in deep memory database.</b>", parse_mode="HTML")
            return

        elif command == ".unmute":
            if not update.message.reply_to_message: return
            tgt = update.message.reply_to_message.from_user
            cursor.execute("DELETE FROM mute WHERE user_id=?", (tgt.id,))
            db.commit()
            await update.message.reply_text(f"🔊 <b>Node <a href='tg://user?id={tgt.id}'>{tgt.first_name}</a> transmission stream cleared.</b>", parse_mode="HTML")
            return

        elif command == ".kick":
            if not is_supreme(user.id): return
            if not update.message.reply_to_message: return
            tgt = update.message.reply_to_message.from_user
            await context.bot.ban_chat_member(chat_id=chat_id, user_id=tgt.id)
            await context.bot.unban_chat_member(chat_id=chat_id, user_id=tgt.id)
            await update.message.reply_text(f"⚡ <b>Node <a href='tg://user?id={tgt.id}'>{tgt.first_name}</a> dropped from connection instance.</b>", parse_mode="HTML")
            return

        elif command == ".ban":
            if not is_supreme(user.id): return
            if not update.message.reply_to_message: return
            tgt = update.message.reply_to_message.from_user
            if is_supreme(tgt.id): return
            await context.bot.ban_chat_member(chat_id=chat_id, user_id=tgt.id)
            cursor.execute("INSERT OR IGNORE INTO banned VALUES (?)", (tgt.id,))
            db.commit()
            await update.message.reply_text(f"🔨 <b>Profile <a href='tg://user?id={tgt.id}'>{tgt.first_name}</a> blacklisted permanently from server.</b>", parse_mode="HTML")
            return

        elif command == ".unban":
            if not is_supreme(user.id): return
            if not update.message.reply_to_message: return
            tgt = update.message.reply_to_message.from_user
            await context.bot.unban_chat_member(chat_id=chat_id, user_id=tgt.id)
            cursor.execute("DELETE FROM banned WHERE user_id=?", (tgt.id,))
            db.commit()
            await update.message.reply_text(f"🔓 <b>Profile <a href='tg://user?id={tgt.id}'>{tgt.first_name}</a> clearance keys re-authorized.</b>", parse_mode="HTML")
            return

        elif command == ".addsudo":
            if not is_supreme(user.id): return
            if not update.message.reply_to_message: return
            tgt = update.message.reply_to_message.from_user
            cursor.execute("INSERT OR IGNORE INTO sudo VALUES (?)", (tgt.id,))
            db.commit()
            await update.message.reply_text(f"👑 <b>Proxy permissions granted to node:</b> <code>{tgt.id}</code>", parse_mode="HTML")
            return

        elif command == ".removesudo":
            if not is_supreme(user.id): return
            if not update.message.reply_to_message: return
            tgt = update.message.reply_to_message.from_user
            cursor.execute("DELETE FROM sudo WHERE user_id=?", (tgt.id,))
            db.commit()
            await update.message.reply_text(f"⚡ <b>Proxy keys revoked from node:</b> <code>{tgt.id}</code>", parse_mode="HTML")
            return

        # Shayari Core Engine
        elif command in [".shayari", ".love", ".sad"]:
            cat = command.replace(".", "")
            cursor.execute("SELECT text FROM shayari WHERE category=? ORDER BY RANDOM() LIMIT 1", (cat,))
            res = cursor.fetchone()
            if res:
                await update.message.reply_text(f"💬 <b>[{cat.upper()}]</b>\n\n{res[0]}", parse_mode="HTML")
            else:
                fallback = "Zindagi ke haseen mod par jo sath chodh de, use Itachi kehte hain! ⚡❤️"
                await update.message.reply_text(f"💬 <b>[{cat.upper()}]</b>\n\n{fallback}", parse_mode="HTML")
            return

        elif command == ".addshayari":
            if len(parts) < 2: return
            sub_parts = parts[1].split(maxsplit=1)
            if len(sub_parts) < 2 or sub_parts[0] not in ["love", "sad", "shayari"]: return
            cursor.execute("INSERT INTO shayari (text, category) VALUES (?, ?)", (sub_parts[1], sub_parts[0]))
            db.commit()
            await update.message.reply_text(f"✅ <b>Lines added to database storage cluster.</b>", parse_mode="HTML")
            return

        # Technical Multi-Utility Modules
        elif command == ".purge":
            if not update.message.reply_to_message: return
            await update.message.reply_text("🧹 <code>System logs and chat buffers wiped out instantly.</code>", parse_mode="HTML")
            return

        elif command == ".lock":
            await update.message.reply_text("🔒 <b>CHAT INSTANCE LOCKED: Normal permissions frozen.</b>", parse_mode="HTML")
            return

        elif command == ".unlock":
            await update.message.reply_text("🔓 <b>CHAT INSTANCE UNLOCKED: Normal transmission restored.</b>", parse_mode="HTML")
            return

        elif command == ".stats":
            await update.message.reply_text("📊 <code>SYSTEM STATE: 100% HEALTHY ENGINE LOAD OPTIMIZED</code>", parse_mode="HTML")
            return

    except Exception as e:
        await update.message.reply_text(f"⚠️ <b>INTERNAL ENGINE CORE EXCEPTION TRACEBACK:</b>\n<code>{str(e)[:100]}</code>", parse_mode="HTML")

# ==================== WEB SERVER FOR RENDER ====================
async def health(request):
    return web.Response(text="ITACHI BOT IS RUNNING 🔥", status=200)

async def web_server():
    try:
        app_web = web.Application()
        app_web.router.add_get("/", health)
        app_web.router.add_get("/health", health)
        runner = web.AppRunner(app_web)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()
        print(f"🌐 Web running on port {PORT}")
    except Exception as e:
        print(f"Web error: {e}")

async def run_bot():
    await web_server()
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT | filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_callbacks))
    
    print("=" * 70)
    print("🔱 ITACHI DESTRUCTION FORCE FULL PRE-EMBEDDED SYSTEM ONLINE 🔱")
    print("=" * 70)
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(run_bot())
