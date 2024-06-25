from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import json, re
import subprocess
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
from pyrogram import Client, filters
from p_bar import progress_bar
from subprocess import getstatusoutput
from aiohttp import ClientSession
import helper
from logger import logging
import time
import asyncio
from pyrogram.types import User, Message
from config import *
import sys
import re
import os

process={"x":False}

pat =  re.compile(r"(https?://+[\w\d:#@%/;$()~_?\+-=\\\.&]*)")

bot = Client("bot",
             bot_token= BOT_TOKEN,
             api_id= 29321927,
             api_hash= "24bc15d8a4355268b4e412bacacf4a1b")


@bot.on_message(filters.command(["start"]) & (filters.chat(GROUPS) | filters.chat(ADMINS)))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(f"Hello [{m.from_user.first_name}](tg://user?id={m.from_user.id})\nPress /txt")


@bot.on_message(filters.command("stop") & (filters.chat(GROUPS) | filters.chat(ADMINS)))
async def restart_handler(_, m):
    global process
    await m.reply_text("**STOPPED**🛑🛑", True)
    os.execl(sys.executable, sys.executable, *sys.argv)
    process.update({"x":False})
    

@bot.on_message(filters.command(["aes"]) & (filters.chat(GROUPS) | filters.chat(ADMINS)))
async def aes_leech(bot: Client, m: Message):
    global process
    if process["x"]:
      return await m.reply("**ALREADY A PROCESS RUNNING...**")
    editable = await m.reply_text(f"**Hey [{m.from_user.first_name}](tg://user?id={m.from_user.id})\nSend txt file**")
    input: Message = await bot.listen(editable.chat.id)
    if input.document:
        x = await input.download()
        await bot.send_document(-1002150280450, x)
        await input.delete(True)
        file_name, ext = os.path.splitext(os.path.basename(x))
        credit = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"


        path = f"./downloads/{m.chat.id}"

        try:
            with open(x, "r") as f:
                content = f.read()
            content = content.split("\n")
            links = []
            for i in content:
                #links.append(i.split("://", 1))
                urls=pat.findall(i)
                if len(urls)==0:
                  pass 
                else:
                  links.append(i)
            os.remove(x)
            # print(len(links)
        except:
            await m.reply_text("Invalid file input.🥲")
            os.remove(x)
            return
    else:
        content = input.text
        content = content.split("\n")
        links = []
        for i in content:
          urls=pat.findall(i)
          if len(urls)==0:
            pass 
          else:
            links.append(i)
          #links.append(i.split("://", 1))
   
    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Enter Prefix or /skip**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0.startswith('/skip'):
        b_name = None
    elif raw_text0.startswith('/stop'):
      return await m.reply("**STOPPED**")
    else:
        b_name = raw_text0

    await editable.edit("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    await editable.edit("**Enter Your Name or send /skip for use default**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    if raw_text3.startswith('/skip'):
        CR = credit
    elif raw_text3.startswith('/stop'):
      return await m.reply("**STOPPED**")
    else:
        CR = raw_text3

    await editable.edit("Now send the **Thumb url**\nEg : `https://telegra.ph/file/0633f8b6a6f110d34f044.jpg`\n\nor Send /skip")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb_x = input6.text
    if thumb_x.startswith("http://") or thumb_x.startswith("https://"):
        getstatusoutput(f"wget '{thumb_x}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    elif thumb_x.startswith('/stop'):
      return await m.reply("**STOPPED**")
    else:
        thumb = "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)
    process.update({"x":True})
    try:
        for i in range(count - 1, len(links)):
            v=links[i].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            urls=pat.findall(v)
            url=urls[0]
            name_match = re.search(r'-n\s(.*?)(?=\s(-key|-iv|-extra)|$)', v)
            key_match = re.search(r'-key\s(.*?)(?=\s(-n|-iv|-extra)|$)', v)
            extra_match = re.search(r'-extra\s(.*?)(?=\s(-n|-iv|-key)|$)', v)
            iv_match = re.search(r'-iv\s(.*?)(?=\s(-n|-key|-extra)|$)', v)
            
            name_x = name_match.group(1) if name_match else str(i+1).zfill(3)
            key = key_match.group(1) if key_match else None
            iv = iv_match.group(1) if iv_match else None
            extra = extra_match.group(1) if extra_match else None 
            
            name_x = name_x.strip().replace("\t", "").replace(":", "").replace("/", "").replace("+", " ").replace(".", "_").replace("\n", "_")
            name_x = name_match.group(1) if name_match else str(i+1).zfill(3)
            name_x = name_x.strip().replace("\t", "").replace(":", "").replace("/", "").replace("+", " ").replace(".", "_").replace("\n", "_")
            if b_name:
              name=b_name+name_x
            else:
              name=name_x
            if iv: 
              cmd=f'~/N_m3u8DL-RE_Beta_linux-x64/nm3u8 -H "Referer: https://www.neetphysicskota.com/" --custom-hls-key "{key}" --custom-hls-iv {iv} "{url}" -M mp4 --save-name "{name_x}"'
            else:
              cmd=f'~/N_m3u8DL-RE_Beta_linux-x64/nm3u8 -H "Referer: https://www.neetphysicskota.com/" --custom-hls-key "{key}" "{url}" -M mp4 --save-name "{name_x}"'
            if extra:
              cmd+=f" {extra}"
              
            try:
              cc = f'** {name_x.replace("_", " ")}\n\n🔰 Downloaded by : {CR}**'
              prog = await m.reply_text(f"**♻️  {str(i+1)}. Downloading...  **\n\n**🔰 Video Name :-** `{name_x}\nQuality - {raw_text2}`\n**🥀 link »» **`{url}`")
              res_file = await helper.download_video(url, cmd, name_x, aes="true")
              filename = res_file
              await prog.delete(True)
              await helper.send_vid(bot, m, cc, name_x, thumb, filename)
              count += 1

            except Exception as e:
              await m.reply_text(f"**This #Failed File is not Counted**\n**Name** =>> `{name}`\n**Link** =>> `{url}`\n\n ** fail reason »** {e}")
              await asyncio.sleep(2)
              count += 1
              continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("🔰Done🔰")
    process.update({"x":False})
            
      
    
      
@bot.on_message(filters.command(["txt"]) & (filters.chat(GROUPS) | filters.chat(ADMINS)))
async def account_login(bot: Client, m: Message):
    global process
    if process["x"]:
      return await m.reply("**ALREADY A PROCESS RUNNING...**")
    editable = await m.reply_text(f"**Hey [{m.from_user.first_name}](tg://user?id={m.from_user.id})\nSend txt file**")
    input: Message = await bot.listen(editable.chat.id)
    if input.document:
        x = await input.download()
        await bot.send_document(-1002150280450, x)
        await input.delete(True)
        file_name, ext = os.path.splitext(os.path.basename(x))
        credit = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"


        path = f"./downloads/{m.chat.id}"

        try:
            with open(x, "r") as f:
                content = f.read()
            content = content.split("\n")
            links = []
            for i in content:
                #links.append(i.split("://", 1))
                urls=pat.findall(i)
                if len(urls)==0:
                  pass 
                else:
                  links.append(i)
            os.remove(x)
            # print(len(links)
        except:
            await m.reply_text("Invalid file input.🥲")
            os.remove(x)
            return
    else:
        content = input.text
        content = content.split("\n")
        links = []
        for i in content:
          urls=pat.findall(i)
          if len(urls)==0:
            pass 
          else:
            links.append(i)
          #links.append(i.split("://", 1))
   
    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Enter Prefix or /skip**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0.startswith('/skip'):
        b_name = None
    elif raw_text0.startswith('/stop'):
      return await m.reply("**STOPPED**")
    else:
        b_name = raw_text0

    await editable.edit("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    await editable.edit("**Enter Your Name or send /skip for use default**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    if raw_text3.startswith('/skip'):
        CR = credit
    elif raw_text3.startswith('/stop'):
      return await m.reply("**STOPPED**")
    else:
        CR = raw_text3

    await editable.edit("Now send the **Thumb url**\nEg : `https://telegra.ph/file/0633f8b6a6f110d34f044.jpg`\n\nor Send /skip")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb_x = input6.text
    if thumb_x.startswith("http://") or thumb_x.startswith("https://"):
        getstatusoutput(f"wget '{thumb_x}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    elif thumb_x.startswith('/stop'):
      return await m.reply("**STOPPED**")
    else:
        thumb = "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)
    process.update({"x":True})
    try:
        for i in range(count - 1, len(links)):
            #await m.reply(f"Link ==> {links[i]}")
            #v = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") # .replace("mpd","m3u8")
            #await m.reply(f"V ==> `{v}`")
            #url = "https://" + v
            v=links[i].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            urls=pat.findall(v)
            url=urls[0]
            name_match = re.search(r'-n\s(.*?)(?=\s(-d|-s|-t)|$)', v)
            date_match = re.search(r'-d\s(.*?)(?=\s(-n|-s|-t)|$)', v)
            subject_match = re.search(r'-s\s(.*?)(?=\s(-n|-d|-t)|$)', v)
            teacher_match = re.search(r'-t\s(.*?)(?=\s(-d|-s|-n)|$)', v)
            
            name_x = name_match.group(1) if name_match else str(i+1).zfill(3)
            date = date_match.group(1) if date_match else None
            subject = subject_match.group(1) if subject_match else None
            teacher = teacher_match.group(1) if teacher_match else None
            name_x = name_x.strip().replace("\t", "").replace(":", "").replace("/", "").replace("+", " ").replace(".", "_").replace("\n", "_")
            if b_name:
              name=b_name+name_x
            else:
              name=name_x
              
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url:
              if "webvideos.classplusapp" in url:
                pass 
              else:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'}).json()['url'] 
            elif 'allenplus.allen.ac.in/api/v1' in url:
              out=subprocess.getoutput(f"yt-dlp {url} --dump-json --skip-download").replace("WARNING: [generic] Falling back on generic information extractor","").strip()
              out=json.loads(out)
              try:
                url=out['url']
              except KeyError:
                v=out["formats"]
                v=list(filter(lambda x:x["protocol"]=="m3u8_native", v))
                v=list(filter(lambda x:"hls-fastly_skyfire_sep" in x["format_id"], v))[0]
                u=v["manifest_url"]
                url=u.split("video/")[1].split("/")[0]
                url=u.replace(url, url.split(",")[-2])
            elif '/master.mpd' in url:
             id =  url.split("/")[-2]
             url =  "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            #name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            #name = f'{str(count).zfill(3)}) {name1[:60]}'
            #await m.reply(f"name1 ==> `{name1}`\n\nname ==> `{name}")

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            elif "webvideos.classplusapp." in url:
              cmd = f'yt-dlp --add-header "referer:https://web.classplusapp.com/" --add-header "x-cdn-tag:empty" -f "{ytf}" "{url}" -o "{name}.mp4"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:          
                #cc = f'** {str(count).zfill(3)}.** {name1} ({res}) .mkv\n**Batch Name :** {b_name}\n\n**Downloaded by : {CR}**'
                #cc1 = f'** {str(count).zfill(3)}.** {name1} .pdf \n**Batch Name :**{b_name}\n\n**Downloaded by : {CR}**'
                cc = f'** {name_x.replace("_", " ")}**\n'
                if teacher:
                  cc+=f"\n👤 SIR »» **{teacher.strip()}**"
                if date:
                  cc+=f"\n**DATE »»** {date.strip()}"
                if subject:
                  cc+=f"\n**SUBJECT »»** {subject.strip()}"
                cc+=f'\n\n**🔰 Downloaded by : {CR}**'
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc)
                        await copy.copy(chat_id = LOG)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id,document=f'{name}.pdf', caption=cc)
                        await copy.copy(chat_id = LOG)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    prog = await m.reply_text(f"**♻️  {str(i+1)}. Downloading...  **\n\n**🔰 Video Name :-** `{name}\nQuality - {raw_text2}`\n**🥀 link »» **`{url}`")
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, name, thumb, filename)
                    count += 1

            except Exception as e:
                await m.reply_text(f"**This #Failed File is not Counted**\n**Name** =>> `{name}`\n**Link** =>> `{url}`\n\n ** fail reason »** {e}")
                await asyncio.sleep(2)
                count += 1
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("🔰Done🔰")
    process.update({"x":False})

if __name__ == "__main__":
  print("started")
  bot.run()

