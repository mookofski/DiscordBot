import asyncio


class Observer:
    def __init__(self, name):
        self.name = name

    async def Operation():
        await asyncio.wait(1)


class Event:
    def __init__(self):
        self.Observers = set()

    def Add(self, tgt):
        self.Observers.add(tgt)

    def Remove(self, tgt):
        self.Observers.discard(tgt)

    async def Invoke(self):
        for b in self.Observers:
            await b.Operation()


class SendMessage(Observer):
    def __init__(self, message, server):
        self.text = message
        self.Server = server

    async def Operation(self):
        await self.Server.send(self.text)


class TimedEvent(Event):
    def Init(self, times, min):
        self.Count = times
        self.Interval = min

    async def Invokeloop(self):
        for a in range(0, self.Count):
            await self.Invoke()
            await asyncio.sleep(self.Interval * 60)
