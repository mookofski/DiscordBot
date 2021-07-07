import discord
import os
import sqlite3

conn=sqlite3.connect('tasks.db')

c=conn.cursor()

client=discord.Client()

@client.event
async def on_ready():
    print('logged as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        a=str
        a=message.content
        print(a)
        c.execute("INSERT INTO task_inst VALUES (?)",(a,))
        conn.commit()
        await message.channel.send('aaa')
    else:
        for b in c.execute('SELECT * FROM task_inst'):
            print(b)




client.run(os.getenv('TOKEN'))
