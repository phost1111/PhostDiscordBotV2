import discord
import asyncio

client = discord.Client()

VERSION = '0.0.0a'
ADMINS = ['139354514091147264']
PREFIX = '!'
ADMINPREFIX = '*'

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await changePlaying('you suffer', 3)

@client.event
async def on_message(message):
    global VERSION
    global ADMINS
    global PREFIX
    global ADMINPREFIX
    if message.content == ('<@' + client.user.id + '>'):
        await sendMessage(message.channel, 'Curent prefix is "' + PREFIX + '"')
    if (message.channel.is_private) & (message.author.id in ADMINS):
        if (message.content.startswith(ADMINPREFIX)) & (message.author.id != client.user.id):
            message.content = message.content[len(ADMINPREFIX):]
            adminargs = message.content.split()
            if (adminargs[0] == 'changePrefix') & (len(adminargs) > 1):
                adminargs.pop(0)
                PREFIX = ' '.join(adminargs, )
    if (message.content.startswith(PREFIX)) & (message.author.id != client.user.id):
        message.content = message.content[len(PREFIX):]
        args = message.content.split()
        if args[0] == 'test':
            await sendMessage(message.channel, client.user.id)
        elif args[0] == 'msgcount':
            counter = 0
            tmp = await sendMessage(message.channel, 'Calculating...')
            async for log in client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
        elif args[0] == 'sleep':
            tmp = await sendMessage(message.channel, 'Sleeping...')
            await asyncio.sleep(15)
            await client.edit_message(tmp, 'Done Sleeping!')
        elif args[0] == 'version':
            await sendMessage(message.channel, VERSION)
        elif args[0] == 'clear':
            isadmintmp = False
            for role in message.author.roles:
                if role.name == 'PhostBotAdmin':
                    isadmintmp = True
                    if len(args) > 1:
                        await client.purge_from(message.channel, limit=int(args[1]))
                    else:
                        await client.purge_from(message.channel)
            if not isadmintmp:
                tmp = await sendMessage(message.channel, 'You are not a PhostBotAdmin')
                tmplist = [tmp, message]
                await asyncio.sleep(3)
                await client.delete_messages(tmplist)
        elif args[0] == 'help':
            await sendMessage(message.channel, ('' + PREFIX + 'help - show all commands\n' + PREFIX + 'msgcount - How many messages have you sent in this channel? (Max 100)\n' + PREFIX + 'version - Which version is the bot on?\n' + PREFIX + 'clear [amount] - clears the last [amount]/100 messages\n'))


async def changePlaying(Text, Type):
    await client.change_presence(game=discord.Game(name=Text, type=Type))

async def sendMessage(channel, messageText):
    await client.send_typing(channel)
    return await client.send_message(channel, messageText)

file = open('token.txt', 'r')
token = file.read()
file.close()
client.run(token)
