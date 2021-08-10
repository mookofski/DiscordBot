from asyncio.windows_events import NULL
from Android.IUser import IUser
from OP_Handler import OPHandler
import asyncio
from asyncio.base_events import Server
import discord
import os
import sqlite3
import Intrepter
from Notifier import *


from discord import message


def GetInstance(user: discord.User, active: list[discord.User], inst: list[OPHandler]):

    if user in active:
        return Instances[ActiveUsers.index(user)]
        pass
    else:
        active.append(user)
        inst.append(OPHandler(user))
        return inst[len(inst) - 1]
        pass

    pass


async def Timeout(inst: list[OPHandler], active: list[discord.User]):
    while True:
        await asyncio.sleep(15 * 60)
        if len(inst) > 0:
            for a in inst:

                if a.Interacted == False:
                    active.remove(a.user)
                    inst.remove(a)
                    print(":REMOVED")
                    pass  # remove
                else:
                    a.Interacted = False
                    pass  # reset
                pass  # inst loop
            pass  # length check

        pass  # loop

    pass


client = discord.Client()

Instances = list[OPHandler]()
ActiveUsers = list[discord.User]()

loop = asyncio.get_event_loop()
TimeoutHandler = loop.create_task(Timeout(Instances, ActiveUsers))



@client.event
async def on_ready():
    print("logged as {0.user}".format(client))
    notifier = Notifier(client)
    notifier.TimeList.append(sqlite3.Time(hour=19, minute=32))
    notifier.TimeList.append(sqlite3.Time(hour=20, minute=32))
    
    await notifier.NotificationLoop()


@client.event
async def on_message(message):

    if message.author == client.user:

        return

    IUser.AddUnique(message.author)

    hnd = GetInstance(message.author, ActiveUsers, Instances)

    command = message.content.split(",")[0].upper()

    if command in OPHandler.Initializers:
        await hnd.Onmessage(message)
        pass

    if message.content.startswith("!ACTIVE"):
        text = str()

        for i in ActiveUsers:
            text += i.name + ":" + i.id.__str__() + "\n"
            pass
        await message.channel.send(text)
        pass

client.run(os.getenv("TOKEN"))
loop.run_until_complete(TimeoutHandler)

