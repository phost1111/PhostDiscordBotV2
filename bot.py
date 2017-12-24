import discord
import cassiopeia as cass
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

client = discord.Client()

open('leaguekey.txt', 'a').close()
with open('leaguekey.txt', 'r') as leaguekeyfile:
    leaguekey = leaguekeyfile.readline()
cass.set_riot_api_key(key=leaguekey)

VERSION = '0.1.0a'
ADMINS = ['139354514091147264']
PREFIX = '!'
ADMINPREFIX = '*'
DELETIONWAITTIME = 5

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
        return
    if (message.channel.is_private) & (message.author.id in ADMINS):
        if (message.content.startswith(ADMINPREFIX)) & (message.author.id != client.user.id):
            message.content = message.content[len(ADMINPREFIX):]
            adminargs = message.content.split()
            if (adminargs[0] == 'changePrefix') & (len(adminargs) > 1):
                adminargs.pop(0)
                PREFIX = ' '.join(adminargs, )
        return
    if (message.content.startswith(PREFIX)) & (message.author.id != client.user.id):
        message.content = message.content[len(PREFIX):]
        args = message.content.split()
        if (args[0] == 'test') & (len(args) > 2):
            tmpmessage = await  sendMessage(message.channel, "Fetchig data from Riot's Servers...")
            tmpregion = args[1]
            args.pop(0)
            args.pop(0)
            tmpsummonername = ' '.join(args)
            summoner = cass.get_summoner(name=tmpsummonername, region=tmpregion)
            match = summoner.current_match
            blueteam = match.blue_team.participants
            redteam = match.red_team.participants
            players = 'Blue Team:```\n'
            for player in blueteam:
                for mastery in player.summoner.champion_masteries:
                    if mastery.champion.id == player.champion.id:
                        players += player.summoner.name + ' (Lvl ' + str(mastery.level) + ' ' + player.champion.name + ')' + '\n'
                        return
            players += '```Red Team:```\n'
            for player in redteam:
                for mastery in player.summoner.champion_masteries:
                    if mastery.champion.id == player.champion.id:
                        players += player.summoner.name + ' (Lvl ' + str(mastery.level) + ' ' + player.champion.name + ')' + '\n'
                        return
            players += '```'
            await client.edit_message(tmpmessage, new_content=players)
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
            tmpisadmin = False
            for role in message.author.roles:
                if role.name == 'PhostBotAdmin':
                    tmpisadmin = True
                    if len(args) > 1:
                        await client.purge_from(message.channel, limit=int(args[1]))
                    else:
                        await client.purge_from(message.channel)
            if not tmpisadmin:
                await sendAndDeleteMessages(message, message.channel, 'You are not a PhostBotAdmin!')
        elif args[0] == 'help':
            await sendMessage(message.channel, ('```' + PREFIX + 'help - show all commands\n' + PREFIX + 'msgcount - How many messages have you sent in this channel? (Max 100)\n' + PREFIX + 'version - Which version is the bot on?\n' + PREFIX + 'clear [amount] - clears the last [amount]/100 messages\n' + PREFIX + 'registerCrossServer - registers the channel this command is issued in to our Cross-Server-System\n' + PREFIX + 'removeCrossServer - removes the channel this command is issued in from our Cross-Server-System\n' + '```'))
        elif args[0] == 'registerCrossServer':
            tmpisadmin = False
            for role in message.author.roles:
                if role.name == 'PhostBotAdmin':
                    tmpisadmin = True
            if not tmpisadmin:
                await sendAndDeleteMessages(message, message.channel, 'You are not a PhostBotAdmin!')
                return
            alreadyInList = False
            for channelid in CROSSSERVERCHANNELS:
                if channelid == message.channel.id:
                    alreadyInList = True
                    break
            if alreadyInList:
                await sendAndDeleteMessages(message, message.channel, 'That channel is already registered!')
                return
            with open('crossserverchannels.txt', 'a') as file:
                file.write(message.channel.id + '\n')
            CROSSSERVERCHANNELS.append(message.channel.id)
            await sendMessage(message.channel, 'Successfully registered this channel for CrossServer use!')
        elif args[0] == 'removeCrossServer':
            tmpisadmin = False
            for role in message.author.roles:
                if role.name == 'PhostBotAdmin':
                    tmpisadmin = True
            if not tmpisadmin:
                await sendAndDeleteMessages(message, message.channel, 'You are not a PhostBotAdmin!')
                return
            CROSSSERVERCHANNELS.remove(message.channel.id)
            with open('crossserverchannels.txt', 'w') as file:
                file.write('\n'.join(CROSSSERVERCHANNELS))
            await sendMessage(message.channel, 'Successfully removed this channel from CrossServer use!')
        return
    if message.author.id != client.user.id:
        for channelid in CROSSSERVERCHANNELS:
            if channelid == message.channel.id:
                tmpcrossserverchannels = CROSSSERVERCHANNELS.copy()
                tmpcrossserverchannels.remove(channelid)
                for channelid2 in tmpcrossserverchannels:
                    tmpembed = discord.Embed(type='rich', description=message.content).set_author(name='@' + message.author.name + '#' + message.author.discriminator, icon_url=message.author.avatar_url)
                    await client.send_message (client.get_channel(channelid2), embed=tmpembed)




async def changePlaying(Text, Type):
    await client.change_presence(game=discord.Game(name=Text, type=Type))

async def sendMessage(channel, messageText):
    await client.send_typing(channel)
    return await client.send_message(channel, messageText)

async def sendAndDeleteMessages(message, channel, messageText):
    tmpmessages = [await sendMessage(channel, messageText), message]
    await asyncio.sleep(DELETIONWAITTIME)
    await client.delete_messages(tmpmessages)

open('token.txt', 'a').close()
open('crossserverchannels.txt', 'a').close()
with open('token.txt', 'r') as tokenfile:
    token = tokenfile.readline()
with open('crossserverchannels.txt', 'r') as crossserverfile:
    CROSSSERVERCHANNELS = crossserverfile.readlines()
    CROSSSERVERCHANNELS = [channelid.strip() for channelid in CROSSSERVERCHANNELS]
client.run(token)