from .client import Client
import numpy as np
from numpy.random import exponential
from numpy import median
import time as tim
import asyncio

class Team_11_Bot(Client):
    def __init__(self):
        super().__init__()
        self.name = "Zoe" #Your Bot's Name
        # Your Initialization Code Here
        self.my_last_bid = {}
        self.max_bid_history = []
        self.how_many_bids = {}
        self.how_many_my_bids = {}
        self.running = {}
        self.any_run = 0
        pass
    
    async def initial_pay(self):
        worked = False
        while(not worked):
            for i in range(1,101):
                await super().start(i)
                diff = np.random.uniform(0.0001,0.01)
                worked = await super().submit_bid(i, diff)
                if worked:
                    self.running[i] = 1
                    self.my_last_bid[i] = diff

    async def pay(self, auction_id, bid):
        tries = 0
        while tries < 5:
            worked = await super().submit_bid(auction_id, bid)
            if worked:
                self.my_last_bid[auction_id] = bid
                return
            await asyncio.sleep(1)
            tries += 1

    async def start(self, auction_id):
        await super().start(auction_id)
        self.my_last_bid[auction_id] = 0
        # if not self.any_run:
            # self.any_run = 1
            # await self.initial_pay()
        self.how_many_my_bids[auction_id] = 0
        self.running[auction_id] = 1

        diff = np.random.uniform(0.0001,0.01)
        await self.pay(auction_id, diff)
        
        while self.running[auction_id]:
            j = self.how_many_my_bids[auction_id]
            if j+1 >= len(self.max_bid_history): 
                await asyncio.sleep(0.25)
                continue
            diff = np.random.uniform(0.01,0.05)
            bid_value = max(1.125*self.my_last_bid[auction_id], self.max_bid_history[j+1] + diff)
            if bid_value < 1:
                await self.pay(auction_id, bid_value)
                self.how_many_my_bids[auction_id] += 1
                await asyncio.sleep(5)
            else:
                await asyncio.sleep(0.25)

            # await asyncio.sleep(max(0,5-(tim.time()-self.my_last_bid_time[auction_id])))
    
    async def receive_bid(self, auction_id, bid_value):
        await super().receive_bid(auction_id, bid_value)
        if auction_id not in self.how_many_bids:
            self.how_many_bids[auction_id] = 0
        self.how_many_bids[auction_id] += 1
        while self.how_many_bids[auction_id] >= len(self.max_bid_history):
            self.max_bid_history.append(bid_value)
        self.max_bid_history[self.how_many_bids[auction_id]] = max(self.max_bid_history[self.how_many_bids[auction_id]], bid_value)
        if self.max_bid_history[self.how_many_bids[auction_id]] == bid_value:
            if self.running[auction_id]:
                diff = np.random.uniform(0.01,0.05)
                to_bid = max(1.125*self.my_last_bid[auction_id], bid_value + diff)
                if to_bid < 1:
                    await self.pay(auction_id, to_bid)

    
    async def end_auction(self, auction_id):
        await super().end_auction(auction_id)
        self.running[auction_id] = 0
        # Your code for ending auction
