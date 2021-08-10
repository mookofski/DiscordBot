import asyncio
from asyncio.windows_events import NULL

from discord import client
import Text
import discord
import sqlite3
from sqlite3 import Time
from ITask import ITask
from Android.IUser import IUser
import time as systime


class Notifier:
    def __init__(self, cli) -> None:
        Notifier.key = "NOTIFIER_UNIT"
        self.client = discord.Client
        self.client = cli
        self.TimeList = list[sqlite3.Time]()
        self.Active = True
        pass

    async def NotificationLoop(self):
        if len(self.TimeList) == 0:
            print("EmptyTimelist")
            return
            pass

        while self.Active:
            if len(self.TimeList) > 0:
                timeuntil = float(10000000000)
                now = TimeofDay()

                for t in self.TimeList:
                    if now != t:
                        next = MinutesUntil(now, t)
                        if timeuntil > next:
                            timeuntil = next
                            pass  # length check
                        pass  # time dupe check
                    pass  # time candidate loop

                pass

            await asyncio.sleep(timeuntil * 60)
            await self.Notify()
            pass  # main loop
        pass  # func

    async def Notify(self):

        UserList = IUser.GetAllUser()
        for user in UserList:
            tasklist = ITask.GetActiveTask(user.name)
            target = discord.User
            target = await self.client.fetch_user(user.id)

            if target != None and IUser.isAdmin(target):
                if len(tasklist) > 0:
                    outputtext = str()

                    for t in tasklist:
                        outputtext += t.__str__()
                        outputtext += "\n"

                        pass  # message construction
                    await target.send(outputtext)

                    pass  # task length check
                pass  # user validity check

        pass  # user list loop

    pass  # main func


def TimeofDay() -> sqlite3.Time:
    now = systime.localtime()

    return sqlite3.Time(hour=now.tm_hour, minute=now.tm_min)
    pass


def MinutesUntil(cur: Time, tgt: Time):

    ch = cur.hour % 24
    th = tgt.hour % 24
    cm = cur.minute % 60
    tm = tgt.minute % 60

    hour = ch - th
    if ch > th:
        hour = 24 - hour
        pass

    if ch == th and cm > tm:
        hour += 23
        pass
    hour = abs(hour)

    minute = cm - tm
    if cm > tm:
        minute = 60 - minute
        pass
        if ch != th:
            hour -= 1

    minute = abs(minute)

    return (hour * 60) + minute
