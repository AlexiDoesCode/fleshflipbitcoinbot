import os
import random
from dotenv import load_dotenv
import blockchain
import urllib.request
import json
from datetime import datetime
import dateutil.parser
import time
import discord
import asyncio
# 1
from discord.ext import commands
from discord.ext.tasks import loop

client = discord.Client()

token = ''
balance = 10000

blockMined = False
# 2
bot = commands.Bot(command_prefix='!')
bot.remove_command("help")
        
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='addr')
async def addr(ctx, address):
    raw = ("http://api.blockcypher.com/v1/btc/main/addrs/" + address)

    json_obj = urllib.request.urlopen(raw)
    data = json.load(json_obj)

    address = data['address']
    balance = data['balance']
    embed = discord.Embed(title="Blockchain Information", description ="", color=0x5ba0d0) 
    embed.add_field(name="Address", value=address, inline=False)
    embed.add_field(name="Balance", value=balance, inline=False)
    await ctx.send(embed=embed)

@bot.command(name='tx')
async def addr(ctx, tx):
    raw = ("http://api.blockcypher.com/v1/btc/main/txs/" + tx)

    json_obj = urllib.request.urlopen(raw)
    data = json.load(json_obj)
    txid = data['hash']

    inputs = data['inputs']
    inputAddress = inputs[0]['addresses']
    outputs = data['outputs']
    outputAddress = outputs[0]['addresses']
    
    confirmations = data['confirmations']
    embed = discord.Embed(title="Blockchain Information", description ="", color=0x5ba0d0) 
    embed.add_field(name="TX Hash", value=txid, inline=False)
    embed.add_field(name="Confirmations", value=confirmations, inline=False)
    embed.add_field(name="Sent from", value=inputAddress, inline=False)
    embed.add_field(name="Received by", value=outputAddress, inline=False)
    await ctx.send(embed=embed)
    
@bot.command(name='help')
async def blk(ctx):
    embed = discord.Embed(title="Help", description ="", color=0x5ba0d0) 
    embed.add_field(name="1. !blk", value="Shows when the previous block was mined", inline=False)
    embed.add_field(name="2. !addr <address>", value="Shows the balance of an address", inline=False)
    embed.add_field(name="3. !mex <coin>", value="Shows the last price of listed coins on BitMEX. CASE SENSITIVE", inline=False)
    embed.add_field(name="4. !list <coins/???>", value="Lists whatever you selected", inline=False)
    embed.add_field(name="5. !tx <TXID>", value="Shows information about the transaction", inline=False)
    await ctx.send(embed=embed)

@bot.command(name='list')
async def blk(ctx, param):
    if param == "coins":
        embed = discord.Embed(title="Listed Coins on Bitmex", description ="", color=0x5ba0d0) 
        embed.add_field(name="BTC", value="XBTUSD", inline=False)
        embed.add_field(name="ETH", value="ETHUSD", inline=False)
        embed.add_field(name="ADA", value="ADAZ19", inline=False)
        embed.add_field(name="BCH", value="BCHZ19", inline=False)
        embed.add_field(name="EOS", value="EOSZ19", inline=False)
        embed.add_field(name="LTC", value="LTCZ19", inline=False)
        embed.add_field(name="TRX", value="TRXZ19", inline=False)
        embed.add_field(name="XRP", value="XRPZ19", inline=False)
        embed.set_thumbnail(url='https://32thcv3s4g2f4bru3o3jkumf-wpengine.netdna-ssl.com/wp-content/uploads/2019/11/BitMEX.png')
    await ctx.send(embed=embed)
    
@bot.command(name='blk')
async def blk(ctx):
    ids = [ "325262878313676812", "264461985444265984", "525412450909290496" ]
    if ctx.message.author.id in ids:
        embed=discord.Embed(title="Bot Creator Permission", description="You don't have permission to use this command.", color=0xe60000)
        await bot.say(embed=embed)
    else:
        blkdata = ("https://api-r.bitcoinchain.com/v1/status")

        json_blk = urllib.request.urlopen(blkdata)
        blk = json.load(json_blk)
        
        BlockTime = blk['time']
        timenow = int(time.time())

        blockTimeUnix = int(timenow) - int(BlockTime)

        minutesLast = time.strftime('%Mm %Ss', time.gmtime(int(blockTimeUnix)))
        block = blk['height']
        
        #embed = discord.Embed(title="Last block mined", description ="", color=0x5ba0d0) 
        #embed.add_field(name="Block", value=str(block), inline=False)
        #embed.add_field(name="Time since last mined", value=str(minutesLast + " ago"), inline=False)
    
        await ctx.send("Seen block #" + str(block) +" "+ str(minutesLast) + " ago")

@bot.command(name='mex')
async def mex(ctx, coin):
    btcdata = ("https://www.bitmex.com/api/v1/trade?symbol=XBT&count=1&reverse=true")
    ethdata = ("https://www.bitmex.com/api/v1/trade?symbol=ETH&count=1&reverse=true")
    adadata = ("https://www.bitmex.com/api/v1/trade?symbol=ADA&count=1&reverse=true")
    bchdata = ("https://www.bitmex.com/api/v1/trade?symbol=BCH&count=1&reverse=true")
    eosdata = ("https://www.bitmex.com/api/v1/trade?symbol=EOS&count=1&reverse=true")
    ltcdata = ("https://www.bitmex.com/api/v1/trade?symbol=LTC&count=1&reverse=true")
    trxdata = ("https://www.bitmex.com/api/v1/trade?symbol=TRX&count=1&reverse=true")
    xrpdata = ("https://www.bitmex.com/api/v1/trade?symbol=XRP&count=1&reverse=true")

    if coin == "BTC":
        mexdata = btcdata
    if coin == "ETH":
        mexdata = ethdata
    if coin == "ADA":
        mexdata = adadata
    if coin == "BCH":
        mexdata = bchdata        
    if coin == "EOS":
        mexdata = eosdata
    if coin == "LTC":
        mexdata = ltcdata
    if coin == "TRX":
        mexdata = trxdata
    if coin == "XRP":
        mexdata = xrpdata
        
    json_mex = urllib.request.urlopen(mexdata)
    mex = json.load(json_mex)

    lastPrice = mex[0]['price']

    embed = discord.Embed(title="Bitmex Prices", description ="", color=0x5ba0d0) 
    embed.add_field(name="Last Price", value=lastPrice, inline=False)
    embed.set_thumbnail(url='https://32thcv3s4g2f4bru3o3jkumf-wpengine.netdna-ssl.com/wp-content/uploads/2019/11/BitMEX.png')
    await ctx.send(embed=embed)
    
@bot.command(name='bal')
async def bal(ctx):
    embed = discord.Embed(title="Server Wallet", description ="", color=0x5ba0d0) 
    embed.add_field(name="Balance", value=balance, inline=False)
    await ctx.send(embed=embed)
@bot.command(name='tip')
async def tip(ctx, amount, user):
    embed = discord.Embed(title="Economy", description ="", color=0x5ba0d0) 
    embed.add_field(name="Transaction", value="Tipped " + amount + " to" + user, inline=False)
    await ctx.send(embed=embed)

@bot.command(name='withdraw')
async def tip(ctx, amount, address):
    embed = discord.Embed(title="Economy", description ="", color=0x5ba0d0) 
    embed.add_field(name="Transaction", value="Withdrawn " + amount + " to " + address, inline=False)
    await ctx.send(embed=embed)


@bot.command(name='heads')
async def h(ctx, bet):
    global balance
    choices = ["heads", "tails"]
    chosen = random.choice(choices)
    balance = int(balance) - int(bet)
    if (chosen == "heads"):
        embed = discord.Embed(title="Coin Flip", description ="", color=0x5ba0d0) 
        embed.add_field(name="Coin tossed heads", value="You won " + bet +"!", inline=False)
        balance = int(balance) + int(bet*2)
    else:
        embed = discord.Embed(title="Coin Flip", description ="", color=0x5ba0d0) 
        embed.add_field(name="Coin tossed tails", value="You lost " + bet, inline=False)
    await ctx.send(embed=embed)
@bot.command(name='tails')
async def t(ctx, bet):
    global balance
    choices = ["heads", "tails"]
    chosen = random.choice(choices)
    balance = int(balance) - int(bet)
    if (chosen == "tails"):
        embed = discord.Embed(title="Coin Flip", description ="", color=0x5ba0d0) 
        embed.add_field(name="Coin tossed tails", value="You won " + bet +"!", inline=False)
        balance = int(balance) + int(bet*2)
    else:
        embed = discord.Embed(title="Coin Flip", description ="", color=0x5ba0d0) 
        embed.add_field(name="Coin tossed heads", value="You lost " + bet, inline=False)
    await ctx.send(embed=embed)
bot.run(token)
