import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

# ========== قائمة الألعاب ==========
@bot.tree.command(name="العاب", description="عرض قائمة الألعاب المتاحة")
async def games_list(interaction: discord.Interaction):
    embed = discord.Embed(title="🎮 قائمة الألعاب", color=0x00ff00)
    embed.add_field(name="/روليت", value="عجلة تختار شخص يطرد شخص آخر", inline=False)
    embed.add_field(name="/روليت_عكسي", value="عجلة تختار شخص ينطرد هو", inline=False)
    embed.add_field(name="/اجمع", value="اجمع الكلمة العربية واحصل على نقاط", inline=False)
    embed.add_field(name="/فكك", value="فكك الكلمة إلى حروف", inline=False)
    await interaction.response.send_message(embed=embed)

# ========== روليت ==========
roulette_players = {}

@bot.tree.command(name="روليت", description="ابدأ لعبة الروليت")
async def roulette(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    roulette_players[guild_id] = []
    await interaction.response.send_message("🎡 لعبة الروليت بدأت! استخدم /انضم للمشاركة، ثم /دور لتدوير العجلة")

@bot.tree.command(name="انضم", description="انضم للعبة الروليت")
async def join(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    if guild_id not in roulette_players:
        await interaction.response.send_message("❌ ما في لعبة نشطة! استخدم /روليت أولاً")
        return
    if interaction.user in roulette_players[guild_id]:
        await interaction.response.send_message("⚠️ أنت منضم أصلاً!")
        return
    roulette_players[guild_id].append(interaction.user)
    await interaction.response.send_message(f"✅ {interaction.user.display_name} انضم للعبة!")

@bot.tree.command(name="دور", description="دور العجلة في الروليت العادي")
async def spin(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    if guild_id not in roulette_players or len(roulette_players[guild_id]) < 2:
        await interaction.response.send_message("❌ تحتاج لاعبين على الأقل!")
        return
    chosen = random.choice(roulette_players[guild_id])
    await interaction.response.send_message(f"🎡 العجلة توقفت عند: **{chosen.display_name}**\nيجب عليه اختيار شخص لطرده!")

# ========== روليت عكسي ==========
@bot.tree.command(name="روليت_عكسي", description="ابدأ لعبة الروليت العكسي")
async def roulette_reverse(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    roulette_players[guild_id] = []
    await interaction.response.send_message("🎡 لعبة الروليت العكسي بدأت! استخدم /انضم للمشاركة، ثم /دور_عكسي")

@bot.tree.command(name="دور_عكسي", description="دور العجلة في الروليت العكسي")
async def spin_reverse(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    if guild_id not in roulette_players or len(roulette_players[guild_id]) < 2:
        await interaction.response.send_message("❌ تحتاج لاعبين على الأقل!")
        return
    chosen = random.choice(roulette_players[guild_id])
    roulette_players[guild_id].remove(chosen)
    await interaction.response.send_message(f"🎡 العجلة توقفت عند: **{chosen.display_name}**\nتم طرده من اللعبة! 👋")

# ========== اجمع ==========
words = {
    "فاكهة": "فواكه",
    "مدرسة": "مدارس",
    "كتاب": "كتب",
    "ولد": "أولاد",
    "بيت": "بيوت",
    "شجرة": "أشجار",
}

points = {}

@bot.tree.command(name="اجمع", description="اجمع الكلمة العربية")
async def collect(interaction: discord.Interaction):
    word = random.choice(list(words.keys()))
    await interaction.response.send_message(f"📝 اجمع هذه الكلمة: **{word}**\nاكتب إجابتك في الشات!")

    def check(m):
        return m.channel == interaction.channel and not m.author.bot

    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
        if msg.content.strip() == words[word]:
            user_id = msg.author.id
            points[user_id] = points.get(user_id, 0) + 10
            await msg.reply(f"✅ إجابة صحيحة! +10 نقاط 🎉\nمجموع نقاطك: {points[user_id]}")
        else:
            await msg.reply(f"❌ خطأ! الإجابة الصحيحة: **{words[word]}**")
    except:
        await interaction.followup.send(f"⏰ انتهى الوقت! الإجابة: **{words[word]}**")

# ========== فكك ==========
@bot.tree.command(name="فكك", description="فكك الكلمة إلى حروف")
async def disassemble(interaction: discord.Interaction):
    words_list = ["ممثل", "مدرسة", "كتاب", "شجرة", "سيارة"]
    word = random.choice(words_list)
    broken = " ".join(list(word))
    await interaction.response.send_message(f"🔤 فكك هذه الكلمة: **{broken}**")

# ========== تشغيل البوت ==========
import os

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"البوت شغال: {bot.user}")

bot.run(os.environ["TOKEN"])
