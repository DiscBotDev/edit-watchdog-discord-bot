#-------------------------------------------
# Edit Watchdog
# Bot analyses edited messages and deletes them if the new message breaks TOS.
# Usecase: Members editing messages to bypass moderator bots restrictions 
#-------------------------------------------

import discord
import re

TOKEN = "PUT YOUR TOKEN HERE!" #Don't erase the double quotes. 

def contains_link(text):
    url_pattern = re.compile(r'(http[s]?://|www\.)+(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+') #Text starting with https/http/www
    if re.search(url_pattern, text):
        return True
    return False


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def fetch_message_from_payload(self,payload):
        channel = await self.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        return message

    async def on_raw_message_edit(self, payload):  # Using on_raw_message_edit instead of raw_message_edit since this can deal with older messages not in internal cache and we aren't concerned with message contents prior to the edit.
        new_message = payload.data
        new_message_content = new_message.get("content","")
        if(contains_link(new_message_content)):
            print(f"{new_message_content} has a link.")
            message = await self.fetch_message_from_payload(payload)
            await message.delete()

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)