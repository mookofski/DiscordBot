import sqlite3
import discord
import os
import Reader
import Notifier
from User import User as usr
client=discord.Client()

conn=sqlite3.connect('task.db')

c=conn.cursor()

usr.AddUnique(usr(223,'test1'),c)



#g=Reader.UserList(c)
#n=Notifier.Notifier(c)
#for i in g.List:
#	print(i.Name)
#	print(len(i.Task_Que))
#	for a in i.Task_Que:			
	#		print(a.Name)
#print(Reader.Task.GetAll(c))
#c.execute('''CREATE TABLE _USERS(id integer PRIMARY KEY,name text)''')

#c.execute('''
#INSERT INTO _USER VALUES(?,?)
#''',)



v=0


conn.commit()
@client.event
async def on_ready():
	print('suc')
	print(type(client.user))
	#await n.AllUser()
	
@client.event
async def on_message(message):
	
	if message.author==client.user:
		return
	usr.AddUnique(usr(message.author.id,message.author.Username),c)
	await message.author.send('aa')
	pass
client.run('ODYyMzIzODA4ODUzNjg4MzM0.YOWroQ.Z0h7pbn1620sTkff2TjErLa5Asw')