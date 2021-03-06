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

VERSION = '0.3.5a'
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
        await sendMessage(message.channel, 'Current prefix is "' + PREFIX + '"')
        return
    if message.channel.is_private & (message.author.id in ADMINS):
        if (message.content.startswith(ADMINPREFIX)) & (message.author.id != client.user.id):
            message.content = message.content[len(ADMINPREFIX):]
            adminargs = message.content.split()
            if adminargs[0] == 'help':
                tmpembed = discord.Embed(color=0xff0000)
                tmpembed.add_field(name=ADMINPREFIX + 'help', value='Show the admin commands', inline=False)
                tmpembed.add_field(name=ADMINPREFIX + 'addAdmin [userID]', value='Add another Admin to the bot (resets on bot restart)', inline=False)
                tmpembed.add_field(name=ADMINPREFIX + 'removeAdmin [userID]', value='Remove another Admin from the bot', inline=False)
                tmpembed.add_field(name=ADMINPREFIX + 'listAdmin', value='List all Admin-IDs', inline=False)
                tmpembed.add_field(name=ADMINPREFIX + 'changePrefix [prefix]', value='Change global prefix of the bot', inline=False)
                tmpembed.add_field(name=ADMINPREFIX + 'changePlaying [id] [status]', value="Change the bot's status", inline=False)
                tmpembed.add_field(name=ADMINPREFIX + 'addCrossServer [channelID]', value='Add Channel to CrossServer-System', inline=False)
                tmpembed.add_field(name=ADMINPREFIX + 'removeCrossServer [channelID]', value='Remove Channel from CrossServer-System', inline=False)
                tmpembed.add_field(name=ADMINPREFIX + 'listCrossServer', value='List all CrossServer-Channel-IDs', inline=False)
                await client.send_message(message.channel, embed=tmpembed)
            elif (adminargs[0] == 'addAdmin') & (len(adminargs) > 1):
                ADMINS.append(adminargs[1])
            elif (adminargs[0] == 'removeAdmin') & (len(adminargs) > 1):
                ADMINS.remove(adminargs[1])
            elif adminargs[0] == 'listAdmin':
                await sendMessage(message.channel, '\n'.join(ADMINS))
            elif (adminargs[0] == 'changePrefix') & (len(adminargs) > 1):
                adminargs.pop(0)
                PREFIX = ' '.join(adminargs, )
            elif (adminargs[0] == 'changePlaying') & (len(adminargs) > 2):
                adminargs.pop(0)
                tmptype = adminargs[0]
                adminargs.pop(0)
                tmptext = ' '.join(adminargs)
                await changePlaying(tmptext, int(tmptype))
            elif (adminargs[0] == 'addCrossServer') & (len(adminargs) > 1):
                tmpchannel = client.get_channel(adminargs[1])
                if not tmpchannel == None:
                    CROSSSERVERCHANNELS.append(adminargs[1])
                    with open('crossserverchannels.txt', 'w') as file:
                        file.write('\n'.join(CROSSSERVERCHANNELS))
            elif (adminargs[0] == 'removeCrossServer') & (len(adminargs) > 1):
                CROSSSERVERCHANNELS.remove(adminargs[1])
                with open('crossserverchannels.txt', 'w') as file:
                    file.write('\n'.join(CROSSSERVERCHANNELS))
            elif adminargs[0] == 'listCrossServer':
                await sendMessage(message.channel, '\n'.join(CROSSSERVERCHANNELS))
        return
    if (message.content.startswith(PREFIX)) & (message.author.id != client.user.id):
        message.content = message.content[len(PREFIX):]
        args = message.content.split()
        if (args[0] == 'test'):
            tmpembed = discord.Embed(title='title', color=0xff0000, description='description').set_author(name='auhorname').set_footer(text='footertext').add_field(name='fieldname', value='fieldvalue').add_field(name='fieldname', value='fieldvalue')
            await client.send_message(message.channel, 'teeest', embed=tmpembed)
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
            tmpembed = discord.Embed(color=0xff0000)
            tmpembed.add_field(name=PREFIX + 'help', value='show all commands', inline=False)
            tmpembed.add_field(name=PREFIX + 'msgcount', value='How many messages have you sent in this channel? (Max 100)', inline=False)
            tmpembed.add_field(name=PREFIX + 'version', value='Which version is the bot on?', inline=False)
            tmpembed.add_field(name=PREFIX + 'clear [amount]', value='clears the last [amount / 100] messages', inline=False)
            tmpembed.add_field(name=PREFIX + 'registerCrossServer', value='registers the channel this command is issued in to our Cross-Server-System', inline=False)
            tmpembed.add_field(name=PREFIX + 'removeCrossServer', value='removes the channel this command is issued in from our Cross-Server-System', inline=False)
            tmpembed.add_field(name=PREFIX + 'lol [~~match~~/summoner] (REGION) (summoner)', value='get a current LoL ~~match /~~ player', inline=False)
            await client.send_message(message.channel, embed=tmpembed)
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
            CROSSSERVERCHANNELS.append(message.channel.id)
            with open('crossserverchannels.txt', 'w') as file:
                file.write('\n'.join(CROSSSERVERCHANNELS))
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
        elif args[0] == 'lol':
            if args[1] == 'match':
                await sendMessage(message.channel, 'The matchlookup is currently disabled due to a fatal bot crash caused by this.')
                return
                # noinspection PyUnreachableCode
                if len(args) > 3:
                    tmpregion = args[2]
                    args.pop(0)
                    args.pop(0)
                    args.pop(0)
                    tmpsummonername = ' '.join(args)
                    summoner = cass.get_summoner(name=tmpsummonername, region=tmpregion)
                    match = summoner.current_match
                    tmpmessage = await  sendMessage(message.channel, "Fetchig data from Riot's Servers...")
                    blueteam = match.blue_team.participants
                    redteam = match.red_team.participants
                    blueteamoutput = ''
                    redteamoutput = ''
                    for player in blueteam:
                        tmprank = 'Unranked'
                        for leagueposition in player.summoner.league_positions:
                            if leagueposition.queue.value == 'RANKED_SOLO_5x5':
                                tmprank = leagueposition.tier.value + ' ' + leagueposition.division.value
                                break
                        blueteamoutput += player.summoner.name + ' (' + player.champion.name + '): ' + '``Level ' + str(
                            player.summoner.level) + ' ' + tmprank + '``\n'
                    for player in redteam:
                        tmprank = 'Unranked'
                        for leagueposition in player.summoner.league_positions:
                            if leagueposition.queue.value == 'RANKED_SOLO_5x5':
                                tmprank = leagueposition.tier.value + ' ' + leagueposition.division.value
                                break
                        redteamoutput += player.summoner.name + ' (' + player.champion.name + '): ' + '``Level ' + str(
                            player.summoner.level) + ' ' + tmprank + '``\n'
                    outputEmbed = discord.Embed(color=0xff0000).add_field(name='Blue team', value=blueteamoutput).add_field(name='Red team', value=redteamoutput)
                    await client.edit_message(tmpmessage, ' ', embed=outputEmbed)
            elif args[1] == 'summoner':
                if len(args) > 3:
                    tmpregion = args[2]
                    args.pop(0)
                    args.pop(0)
                    args.pop(0)
                    tmpsummonername = ' '.join(args)
                    summoner = cass.get_summoner(name=tmpsummonername, region=tmpregion)
                    if (not summoner.exists) or (summoner == None):
                        await sendMessage(message.channel, "Couldn't find " + tmpsummonername + ' in ' + tmpregion)
                        return
                    tmpmessage = await sendMessage(message.channel, "Fetching data from Riot's Servers...")
                    tmpsoloq = 'Unranked'
                    tmpflexq = 'Unranked'
                    tmptwisted = 'Unranked'
                    tmptotalmasteryscore = 0
                    tmptotalmasterypoints = 0
                    tmphighestscorepoints = 0
                    tmpoutputembed = discord.Embed(color=0xff0000).set_author(name=summoner.name, icon_url=summoner.profile_icon.url).add_field(name='Level', value=summoner.level, inline=False)
                    for leagueposition in summoner.league_positions:
                        if leagueposition.queue.value == 'RANKED_SOLO_5x5':
                            tmpsoloq = leagueposition.tier.value + ' ' + leagueposition.division.value
                        elif leagueposition.queue.value == 'RANKED_FLEX_SR':
                            tmpflexq = leagueposition.tier.value + ' ' + leagueposition.division.value
                        elif leagueposition.queue.value == 'RANKED_FLEX_TT':
                            tmptwisted = leagueposition.tier.value + ' ' + leagueposition.division.value
                    for mastery in summoner.champion_masteries:
                        tmptotalmasterypoints += mastery.points
                        tmptotalmasteryscore += mastery.level
                        if mastery.points > tmphighestscorepoints:
                            tmphighestchamp = mastery.champion
                            tmphighestscorepoints = mastery.points
                    tmpoutputembed.add_field(name='SoloQ rank', value=tmpsoloq).add_field(name='FlexQ rank', value=tmpflexq).add_field(name='3v3 rank', value=tmptwisted)
                    tmpoutputembed.add_field(name='Total Mastery Score', value= str(tmptotalmasteryscore) + ' (' + str(tmptotalmasterypoints) + ' points)').add_field(name='Highest Mastery Score Champion', value=tmphighestchamp.name + ' (' + str(tmphighestscorepoints) + ' Mastery Points)')
                    await client.edit_message(tmpmessage, ' ', embed=tmpoutputembed)
        return
    if message.author.id != client.user.id:
        for channelid in CROSSSERVERCHANNELS:
            if channelid == message.channel.id:
                tmpcrossserverchannels = CROSSSERVERCHANNELS.copy()
                tmpcrossserverchannels.remove(channelid)
                for channelid2 in tmpcrossserverchannels:
                    tmpembed = discord.Embed(color=0xff0000, description=message.content).set_author(
                        name='@' + message.author.name + '#' + message.author.discriminator,
                        icon_url=message.author.avatar_url)
                    tmpchannel = client.get_channel(channelid2)
                    if tmpchannel is None:
                        CROSSSERVERCHANNELS.remove(channelid2)
                        with open('crossserverchannels.txt', 'w') as file:
                            file.write('\n'.join(CROSSSERVERCHANNELS))
                    else:
                        await client.send_message(tmpchannel, embed=tmpembed)


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