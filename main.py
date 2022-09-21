import lightbulb
import threading
import keep_alive
import hikari
import random
import datetime
import ccDatabase
import os
import json
import schedule
import re


class embedColors:
  green = "#57F287"
  blue = "#3498DB"
  orange = "#E67E22"
  red = "#ED4245"


class color:

  red = "\033[1;31m"
  green = "\033[1;;32m"
  blue = "\033[4;;34m"


#format date and time for uptime commands
print(datetime.datetime.now())
dtstr = "2022-09-06 14:27:47"
global dt_formatted
dt_formatted = datetime.datetime.fromisoformat(dtstr)
global startTime
startTime = datetime.datetime.now(dt_formatted.tzinfo)

# global variables #
global version
version = "1.4.0"

global lines
lines = str(937 + 173)  #str([main.py] + [ccDatabase.py])

global statusSTR
statusSTR = "/seecoins | Version " + version + " | " + lines + " lines of code"

global cc
cc = ccDatabase.ccDatabase()
cc.loadCCDatabase()

# SET IF MAKING CHANGES
global developing
developing = False


def consoleLog(type, message):
  if type == color.red:

      print(type + " - " + message + " ✗" + "\033[0m")
  if type == color.green:
      print(type + " - " + message + " ✓" + "\033[0m")
  else:
      print("\033[1m" + type + " * " + message + "\033[0m")


bot = lightbulb.BotApp(
    token="MTAxNTY0MjI4MDc2MzMzMDYxMA.GP_nLB.PBnqnYiXldxmABE9SInSpCmJTWydGwRU9knpV0",
    #default_enabled_guilds=(985315511728492616)
    #default enabled guilds: remove after testing.)
)
###############################
#        Miriad Bot           #
#       Version 1.3.0         #
# created by thedankboi_#2556 #
###############################

global rest
rest = hikari.RESTApp()

global rules
rules = {
    "1":
    "We run on a three strike policy. If you get three strikes you will be muted for 24 hours. If you are muted three times you will be banned from the server. If an admin believes an incident requires a higher level of punsihment you may be banned without a warning",
    "2":
    "Follow Discord TOS/Community Guidelines. If you are unsure about a rule, ask moderators before posting.",
    "3":
    "Do not make jokes aimed towards people based on their disability, race, gender, sexuality, etc. If someone makes a joke towards you report it to an <@&942477754056728655> and they will issue a sanction where neccessary.",
    "4":
    "Do not post ANY personal information such as names, addresses, phone numbers, emails, private usernames, passwords or any form of card and bank information. This goes for both your own and others. Exercise basic internet safety.",
    "5":
    "Deleting a message you know is against the rules of a server still counts as breaking the server rules. No matter how fast you delete it, the moderators will still see it.",
    "6":
    "No difficult to ping names such as fancy font(ex. 𝐔ᔕᗴℝᑎⒶ𝓜€, 🅄🅂🄴🅁🄽🄰🄼🄴, υʂҽɾɳαɱҽ) until discord fixes different font character pings.",
    "6.1":
    "The staff have the right to change your nickname(this will only affect this server) without warning. This is to enable you to be pinged where neccessary",
    "7":
    "Self promotion will only happen in <#1009555289936236665>. If you self promote anywhere else you will get a warning."
}

#
global rulesLength
rulesLength = []
# -- Paths to files -- #
global config
config = r"config.txt"

global doneList
doneList = r"doneRoles.txt"

# -- Create functions -- #
hikari.presences.RichActivity.name = "Version " + version


def getSetting():
  #print("exists"+""+Setpath)
  consoleLog(color.blue, "Do setting")
  #time.sleep(5)
  setFile = open(config, 'r')
  #global allSettings

  content = setFile.read()
  global channelID
  channelID = 0
  global hasIntro
  hasIntro = 0
  global roleToAdd
  roleToAdd = 0
  exec(content)
  consoleLog(color.green, "Setting done")
  #print(content)


#log message in channel #transactions
async def logMessage(content):
  await bot.rest.create_message(998700348086681720, content=content)


async def doTax():
  cc.addTaxes("942477753536634962", 10)
  embed = hikari.Embed(
      title="10 CC distributed",
      description=
      "It's Sunday! 10cc was distributed to accounts that are enabled")
  await logMessage(embed)


schedule.every().sunday.at("01:00").do(doTax, 'Adding CC')


async def log(content):
  log_channel = 998700348086681720
  await bot.rest.create_message(log_channel, content=content)


def randomColor():
  colors = [
      "57F287", "3498DB", "9B59B6", "F1C40F", "E67E22", "34495E", "FFFF00",
      "1ABC9C", "5865F2", "EB459E"
  ]
  col = random.randint(0, 6)
  return "#" + colors[col]


#push settings to config.txt
def pushSettings(channelID, hasIntro, roleToAdd):
  consoleLog(color.blue, "Do config")
  setFile = open(r"config.txt", 'w')
  setFile.write("global channelID \nchannelID=" + str(channelID) +
                "\nglobal hasIntro \nhasIntro=" + str(hasIntro) +
                "\nglobal roleToAdd\nroleToAdd=" + str(roleToAdd))
  consoleLog(color.green, "Push Setting Complete")
  #print("global channelID \nchannelID=" + str(channelID) +
  #      "\nglobal hasIntro \nhasIntro=" + str(hasIntro) +
  #      "\nglobal roleToAdd\nroleToAdd=" + str(roleToAdd))
  setFile.close()


#check if author.id is in doneList
def checkForAuthor(authorID):
  doneRoles = open(doneList, 'r')
  content = doneRoles.read()
  if authorID in content:
      return True
  else:
      return False


#write to doneRoles.txt
#weird name but it works
def writeToDoneRoles(authorID):
    doneRoles = open(doneList, "a")
    doneRoles.write(authorID)


# -- Leaderboard Commands -- #


#create leaderboard embed
def sendLeaderboard():
    consoleLog(color.blue, "Do leaderboard")
    try:
        randC = randomColor()
        guild = "942477753536634962"
        leaderboard = cc.getLeaderboard(guild)
        #rank counter
        place = 1
        embed = hikari.Embed(title="Leaderboard",
                             description="Creamcoin Leaderboard",
                             color=randC)
        for key in leaderboard:
            if place > 10:
                break
            else:
                keyStr = str(key)
                #print(keyStr)
                value1 = str(key)
                coins = str(cc.seeCoins(guild, key))
                embed.add_field(
                    str(place) + ": ",
                    f"<@!" + keyStr + "> - " + coins + " cc")
                embed.set_footer(
                    "This leaderboard auto updates. Run /update | color: " +
                    randC)
                consoleLog(color.green, "place: " + str(place))
                place += 1

        return embed
    except:
        consoleLog(color.red, "Leaderboard Error")


async def retrieveUsernames():
    consoleLog(color.blue, "do get usernames")
    guild = "942477753536634962"
    creamCoin = cc.creamCoinReturn()
    for key in creamCoin[guild]:
        UserObject = await bot.rest.fetch_user(int(key))
        try:
            if not UserObject == cc.getUsername(guild, str(key)):
                consoleLog(color.green, "updated username")
        except:
            pass
        name = UserObject.username
        try:
            creamCoin[guild][key]["username"] = name
        except:
            creamCoin[guild][key].add("username", name)
    consoleLog(color.green, "usernames loaded")
    cc.pushCCDatabase()


    #RETURN EMBED WITH RULES
def getRules():
    consoleLog(color.blue, "Do get rules")
    randC = "#3498DB"
    embed = hikari.Embed(title="Rules",
                         description="Server Rules",
                         color=embedColors.blue)
    for key in rules:
        #print(rules[key])
        embed.add_field(str(key), rules[key])
        rulesLength.append(key)
        consoleLog(color.green, "done rule" + key)
    embed.set_footer("/rule [rule] | color: " + randC)
    return embed


# -- Load Events -- #
@bot.listen(hikari.StartedEvent)
async def bot_started(event):
    #set now for start message in #1015726410175889489
    await retrieveUsernames()
    randC = randomColor()
    now = datetime.datetime.now()
    embed = hikari.Embed(title="Bot has started",
                         description="Bot has started at " + str(now.hour) +
                         ":" + str(now.minute) + ":" + str(now.second),
                         color=randC)
    embed.set_thumbnail("miriad.png")
    embed.set_footer("color: " + randC)
    if not developing:
        await bot.rest.create_message(1015726410175889489, content=embed)

    #config
    await bot.rest.edit_message(channel=942477754287411241,
                                message=1020010746433785967,
                                content=getRules())

    getSetting()

    # CREATE LEADERBOARD
    leaderboardChannel = 998697615506030602
    creamCoin = cc.creamCoinReturn()
    #UPDATE LEADERBOARD
    leaderboardID = creamCoin["storage"]["leaderboard"]
    #print(cc.addTaxes("942477753536634962", 100))
    await bot.rest.edit_message(channel=leaderboardChannel,
                                message=leaderboardID,
                                content=sendLeaderboard())
    consoleLog(color.green, "updated leaderboard")
    if developing == True:
        hikariStatus = hikari.Status.DO_NOT_DISTURB
        consoleLog(color.green, "developing == True")
    else:
        hikariStatus = hikari.Status.ONLINE
        consoleLog(color.green, "developing == False")
    #set discord presence
    await bot.update_presence(status=hikariStatus,
                              activity=hikari.Activity(
                                  name=statusSTR,
                                  type=hikari.ActivityType.PLAYING,
                              ))
    consoleLog(color.green, "set status")


@bot.listen(hikari.GuildMessageCreateEvent)
async def messageCreated(event):

    if event.channel_id == 942477754287411245:
        guild = "942477753536634962"
        inputString = event.content
        levelSplit = inputString.split("j", 1)
        levelTwo = levelSplit[1]
        levelOne = levelSplit[0]

        user = int(re.search(r'\d+', levelOne).group())
        level = int(re.search(r'\d+', levelTwo).group())
        randC = randomColor()
        logmessage = hikari.Embed(title="Level Up!",
                                  color=embedColors.green,
                                  description=f"<@{user}> leveled up!")

        if level > 10:
            amount_to_add = 50
            balance = cc.seeCoins(guild, str(user))
            print(balance)
            amount = int(amount_to_add) + int(balance)
            cc.setCoins(guild, str(user), amount, "624384023132635146")
            logmessage.add_field("Level Up!: ",
                                 "+" + str(amount_to_add) + " cream coins")
            cc.pushCCDatabase()
            await logMessage(logmessage)
            #addCoins
        elif level < 10:
            amount_to_add = 20
            balance = cc.seeCoins(guild, str(user))
            print(balance)
            amount = int(amount_to_add) + int(balance)
            cc.setCoins(guild, str(user), amount, "624384023132635146")
            logmessage.add_field("Level Up!: ",
                                 "+" + str(amount_to_add) + " cream coins")
            cc.pushCCDatabase()
            await logMessage(logmessage)
        else:
            print("uh oh")

            #uh oh


# -- Load Commands -- #

event = threading.Event()


@bot.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(16))
@lightbulb.option("seconds",
                  "time to run the poll for(seconds)",
                  type=hikari.OptionType.INTEGER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.option("minutes",
                  "time to run the poll for(minutes)",
                  type=hikari.OptionType.INTEGER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.option("hours",
                  "time to run the poll for(hours)",
                  type=hikari.OptionType.INTEGER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.option("option_2",
                  "option 2",
                  type=hikari.OptionType.STRING,
                  modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.option("option_1",
                  "option 1",
                  type=hikari.OptionType.STRING,
                  modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("poll", "make a poll", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def poll(ctx):
  #initialize variables
  channel = ctx.channel_id
  guild = str(ctx.guild_id)
  emoji_1 = ":one:"
  emoji_2 = ":two:"
  option_1 = str(ctx.options.option_1)
  option_2 = str(ctx.options.option_2)
  #check if not admin
  if not cc.isAdmin(guild, ctx.author.id):
      embed = hikari.Embed(
          title="No perms",
          description=
          "Sorry - you don't have admin perms in the database. We do this to save processing power",
          color=embedColors.red)
      ctx.respond(embed)
      return
  #time variables
  minutes = (ctx.options.minutes) * 60

  hours = (ctx.options.hours) * 3600

  seconds = ctx.options.seconds

  time = seconds + minutes + hours
  #get embed
  embed = (hikari.Embed(
      title="Poll",
      description=f"{option_1}({emoji_1}) or {option_2}({emoji_2})",
      color=embedColors.blue)).set_author(name=ctx.author.username,
                                          icon=ctx.author.display_avatar_url)
  embed.add_field(
      "Open For:",
      f"{ctx.options.hours}:{ctx.options.minutes}:{ctx.options.seconds}")
  #send embed and store in a variable
  rp = await ctx.respond(embed)
  msg = await rp.message()
  one = await msg.add_reaction("1️⃣")
  two = await msg.add_reaction("2️⃣")
  #event.wait(time) #unused wait
  #get message id
  msg_id = msg.id
  
  timeToWait = time
  timeWaited = 0
  Seconds = ctx.options.seconds
  Minutes = ctx.options.minutes
  Hours = ctx.options.hours
  #while loop to let poll responses happen
  while (timeToWait > timeWaited):
      if Seconds <= 0 and Minutes > 0:
          Minutes -= 1
          Seconds = 59
      if Minutes <= 0 and Hours > 0:
          Hours -= 1
          Minutes = 59
      if Hours <= 0 and Minutes <= 0 and Seconds <= 0:
          #when poll is complete
          embed = (hikari.Embed(
          title="Poll",
          color=embedColors.blue,
          description=f"{option_1}({emoji_1}) or {option_2}({emoji_2})")).set_author(
              name=ctx.author.username, icon=ctx.author.display_avatar_url)
          
          embed.add_field("Poll Complete:", f"Results are below")
          await ctx.bot.rest.edit_message(channel=channel,
                                      message=msg_id,
                                      content=embed)
          break #break loop
      #reinitialize embed
      embed = (hikari.Embed(
          title="Poll",
          color=embedColors.blue,
          description=f"{option_1}({emoji_1}) or {option_2}({emoji_2})")).set_author(
              name=ctx.author.username, icon=ctx.author.display_avatar_url)
      embed.add_field("Open For:", f"{Hours}:{Minutes}:{Seconds}")
      embed.set_footer("**Adding other reactions will mess up the poll**")
      #edit message to update count
      await ctx.bot.rest.edit_message(channel=channel,
                                      message=msg_id,
                                      content=embed)
      Seconds = Seconds - 1
      event.wait(1)
  #fetch message object
  msg = await ctx.bot.rest.fetch_message(channel, msg)
  #get reactions list
  reaction = msg.reactions
  #get reaction counts
  oneCount = (reaction[0].count)-1
  twoCount = (reaction[1].count)-1

  #determine which one is greater
  if oneCount > twoCount:
      embed2 = hikari.Embed(title="Poll results",
                            color=embedColors.green,
                            description=f"{option_1} won!")
      embed2.add_field("Standings:", f"{oneCount} - {twoCount}")
      await bot.rest.create_message(channel, content=embed2)
  if oneCount < twoCount:
      embed = hikari.Embed(title="Poll results",
                           color=embedColors.green,
                           description=f"{option_2} won!")
      embed.add_field("Standings:", f"{oneCount} - {twoCount}")
      await bot.rest.create_message(channel, content=embed)
  #if tie  
  if oneCount == twoCount:
      embed = hikari.Embed(title="Poll Results",
                           color=embedColors.orange,
                           description=f"It's a tie!")
      embed.add_field("Standings:", f"{oneCount} - {twoCount}")
      await bot.rest.create_message(channel, content=embed)
  else: #uh oh

    embed = hikari.Embed(title="Error", color=embedColors.red, description="Something happened when retrieving the results")
    embed.add_field("Standings", f"{option_1}: {oneCount}\n{option_2}: {twoCount}")
    await bot.rest.create_message(channel, content=embed)

    
#basic ping command
@bot.command
@lightbulb.command("ping", "says pong", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond("Pong!")


@bot.command
@lightbulb.command("update", "update leaderboard", ephemeral=True,  auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def update(ctx):
    leaderboardChannel = 998697615506030602
    creamCoin = cc.creamCoinReturn()
    #UPDATE LEADERBOARD
    if developing == True:
        hikariStatus = hikari.Status.DO_NOT_DISTURB
    else:
        hikariStatus = hikari.Status.ONLINE
    #set discord presence
    await bot.update_presence(status=hikariStatus,
                              activity=hikari.Activity(
                                  name=statusSTR,
                                  type=hikari.ActivityType.PLAYING,
                              ))
    leaderboardID = creamCoin["storage"]["leaderboard"]
    randC = randomColor()
    await bot.rest.edit_message(channel=leaderboardChannel,
                                message=leaderboardID,
                                content=sendLeaderboard())
    embed = hikari.Embed(title="Success!",
                         description="check the leaderboard channel",
                         color=embedColors.green)
    await ctx.respond(embed)


#uptime command
@bot.command
@lightbulb.command("uptime", "uptime", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def uptime(ctx):
    #get now
    now = datetime.datetime.now()
    #calculate uptime
    uptime = now - startTime
    #make embed and send
    randC = randomColor()
    embed = hikari.Embed(title="Uptime",
                         description="Bot has been up for " + str(uptime),
                         color=randC)
    embed.set_footer("requested by " + ctx.author.mention + " | color: " +
                     randC)
    await ctx.respond(embed)


@bot.command
@lightbulb.option("rule",
                  "rule",
                  type=hikari.OptionType.STRING,
                  modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("rule", "get a rule", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def rule(ctx):
    #get now
    rule = ctx.options.rule
    #make embed and send
    embed = hikari.Embed(title="Rule #" + rule,
                         description="Quoting rule #" + rule +
                         " in <#942477754287411241>",
                         color=randomColor())
    try:
        embed.add_field("Rule " + rule, rules[rule])
    except Exception as e:
        embed.add_field("Rule not found.", "please enter a valid rule")
        embed.add_field("Error: ", e)
    embed.set_footer("requested by  <@" + str(ctx.author.id) + ">")
    await ctx.respond(embed)


#admin command for printing in this channel

##################### LOAD INTRODUCTION COMMANDS #####################


@bot.command
# if user can MANAGE CHANNELS then allow
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(16))
#MANAGE_CHANNELS = 16
@lightbulb.option("channel",
                  "channel",
                  type=hikari.OptionType.CHANNEL,
                  modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("setintrochannel",
                   "set the introduction channel",
                   ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def setintrochannel(ctx):
    channelID = ctx.options.channel.id
    #do something here
    embed = hikari.Embed(title="Introductions Channel",
                         description="Introductions Channel Set:")
    embed.add_field("Channel ID:", channelID)

    embed.set_footer("If this is wrong, run the command again")
    pushSettings(channelID, hasIntro, roleToAdd)
    await ctx.respond(embed)


@bot.command
@lightbulb.command("about", "show information about the bot", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def about(ctx):
    randC = randomColor()
    embed = hikari.Embed(
        title="Miriad Bot",
        description="Miriad Bot is a bot created by  https://thedankboi.tk/ ",
        color=randC)
    embed.add_field("Version:", version)
    embed.set_footer("Requested by " + ctx.author.mention + " color: " + randC)
    await ctx.respond(embed)


@bot.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(16))
@lightbulb.option("nointrorole",
                  "role for people who HAVE NOT done and introduction",
                  type=hikari.OptionType.ROLE,
                  modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.option("introrole",
                  "role for people who HAVE done and introduction",
                  type=hikari.OptionType.ROLE,
                  modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("setintrorole",
                   "the role for people who haven't done an intro",
                   ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def setintrorole(ctx):
    hasIntro = ctx.options.nointrorole.id
    roleToAdd = ctx.options.introrole.id
    hasIntroStr = str(hasIntro)
    embed = hikari.Embed(title="Set Role",
                         description="**successfully added roles**: *" +
                         hasIntroStr + "* and *" + str(roleToAdd) + '*')
    embed.add_field("Have Done An Introduction", ctx.options.introrole.mention)
    embed.add_field("Have *Not* Done An Introduction",
                    ctx.options.nointrorole.mention)
    embed.set_footer("If this is wrong, run the command again")
    pushSettings(channelID, hasIntro, roleToAdd)
    await ctx.respond(embed)
    #hikari.MessageFlag.EPHEMERAL)


@bot.command
#@lightbulb.add_checks.has_role(hasIntro)#if/ role has been added
#, lightbulb.checks.human_only
@lightbulb.add_checks(lightbulb.checks.human_only)
@lightbulb.option("description", "your intro description", required=True)
@lightbulb.option("name", "Your Name", required=True)
@lightbulb.option("age", "Your Age", required=False)
@lightbulb.option("sexuality", "Your Sexuality", required=False)
@lightbulb.option("pronouns", "Your Pronouns", required=True)
@lightbulb.option("likes", "Your Likes", required=False)
@lightbulb.option("dislikes", "Your Dislikes", required=False)
@lightbulb.option("randomfact", "A Random Fact", required=False)
@lightbulb.option("socials", "Your Socials", required=False)
@lightbulb.command(
    "makeintro",
    "make your introduction - leave blank if you dont want to have them",
    ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def makeIntro(ctx):
    user = ctx.author
    randC = randomColor()
    if not checkForAuthor(str(user.id)):
        embed = hikari.Embed(title="Introduction",
                             description=ctx.options.description,
                             color=embedColors.blue)
        embed.add_field("Name:", ctx.options.name)
        if not ctx.options.age == None:
            embed.add_field("Age:", ctx.options.age)
        if not ctx.options.sexuality == None:
            embed.add_field("Sexuality:", ctx.options.sexuality)
        if not ctx.options.pronouns == None:
            embed.add_field("Pronouns", ctx.options.pronouns)
        if not ctx.options.likes == None:
            embed.add_field("Likes", ctx.options.likes)
        if not ctx.options.dislikes == None:
            embed.add_field("Dislikes", ctx.options.dislikes)
        if not ctx.options.randomfact == None:
            embed.add_field("Random Fact", ctx.options.randomfact)
        if not ctx.options.socials == None:
            embed.add_field("Socials", ctx.options.socials)
        embed.set_author(
                name=ctx.author.username, icon=ctx.author.display_avatar_url)
        embed.set_footer("Run by " + str(ctx.author))

        try:
            await bot.rest.add_role_to_member(user=ctx.author,
                                              guild=ctx.guild_id,
                                              role=roleToAdd)
            await bot.rest.create_message(channelID, content=embed)
            embed = hikari.Embed(
                title="Success!",
                color = embedColors.blue,
                description="Successfully created message in channel " +
                str(channelID) + ".")
            writeToDoneRoles(str(user.id))
            await ctx.respond(embed)
        except Exception as e:
            embed = hikari.Embed(title="Error",
                                 color=embedColors.red,
                                 description="Error occured adding roles")
            embed.add_field(
                "Role Error",
                "Make sure I am **above** the desired role to add")
            print(e)
            global globalErrorException
            globalErrorException = e
            row = bot.rest.build_action_row()
            button = row.add_button(hikari.ButtonStyle.PRIMARY, "seeerror")
            button.set_label("See Error Message")
            button.add_to_container()
            await ctx.respond(embed)
    else:
        embed = hikari.Embed(
            title="You've already done an introduction!",
            color=embedColors.red,
            description="Silly goose! You can't do one twice!")
        embed.set_footer("if you think this is a mistake, contact the admin")
        await ctx.respond(embed)


#####################   END INTRODUCTION COMMANDS  #####################
# me when when me when me when me when I when me #
##################### LOAD CREAMCOIN COMMANDS #####################

## ADMIN COMMANDS


@bot.command
@lightbulb.option("user",
                  "user to create",
                  type=hikari.OptionType.USER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.option("disabled",
                  "TRUE OR FALSE",
                  type=hikari.OptionType.BOOLEAN,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.option("admin",
                  "TRUE OR FALSE",
                  type=hikari.OptionType.BOOLEAN,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.command("create", "create user", ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def createUser(ctx):
  user = str(ctx.author.id)
  guild = str(ctx.guild_id)
  target = str(ctx.options.user.id)
  disabled = ctx.options.disabled
  name = (await bot.rest.fetch_user(int(target))).username
  admin = ctx.options.admin
  interaction = cc.create_user(guild, target, disabled, admin, name, user)
  #print(interaction)
  randC = randomColor()
  if interaction == "guildnotfound":
      embed = hikari.Embed(title="Error",
                           description="Guild Not Found.",
                           color=embedColors.red)
      embed.add_field("Error:", "creamCoin.guildnotfound error")
      await ctx.respond(embed)
  if interaction == "noperms":
      embed = hikari.Embed(title="Error",
                           description="You are not admin.",
                           color=embedColors.red)
      embed.add_field("Error:", "creamCoin.noperms error")
      await ctx.respond(embed)
  if interaction == True:
      #print("True")
      embed = hikari.Embed(title="Success!",
                           description="User " + target + " created.")
      await ctx.respond(embed)
  else:
      embed = hikari.Embed(title="User create error",
                           description="Already there bruh",
                           color=embedColors.red)
      await ctx.respond(embed)


@bot.command
@lightbulb.option("user",
                  "user to delete",
                  type=hikari.OptionType.USER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.command("delete", "delete user", ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def deleteUser(ctx):
    user = str(ctx.author.id)
    guild = str(ctx.guild_id)
    target = str(ctx.options.user.id)
    interaction = cc.deleteUser(guild, target, user)
    if interaction == "guildnotfound":
        embed = hikari.Embed(title="Error",
                             description="Guild Not Found.",
                             color=embedColors.red)
        embed.add_field("Error:", "creamCoin.guildnotfound error")
        await ctx.respond(embed)
    if interaction == "noperms":
        embed = hikari.Embed(title="Error",
                             description="You are not admin.",
                             color=embedColors.red)
        embed.add_field("Error:", "creamCoin.noperms error")
        await ctx.respond(embed)
    if interaction == True:
        embed = hikari.Embed(title="Success!",
                             description="User " + target + " deleted.",
                             color=embedColors.green)
        await ctx.respond(embed)


@bot.command
@lightbulb.option("amount",
                  "amount to set coins to",
                  type=hikari.OptionType.INTEGER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.option("user",
                  "the user ",
                  type=hikari.OptionType.USER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.option("log",
                  "if you want to log or not",
                  type=hikari.OptionType.BOOLEAN,
                  required=True)
@lightbulb.command("setcoins", "set coins for a user", ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def setcoins(ctx):
  user = str(ctx.author.id)
  guild = str(ctx.guild_id)
  target = str(ctx.options.user.id)
  targetmention = ctx.options.user
  amount = ctx.options.amount
  interaction = cc.setCoins(guild, target, amount, user)
  if interaction == "noperms":
      embed = hikari.Embed(title="Error",
                           description="You are not admin.",
                           color=embedColors.red)
      embed.add_field("Error:", "creamCoin.noperms error")
      await ctx.respond(embed)
  if interaction == "targetnotfound":
      embed = hikari.Embed(title="Error",
                           description="Target Not Found.",
                           color=embedColors.red)
      embed.add_field("Error:", "creamCoin.targetnotfound error")
      await ctx.respond(embed)
  if interaction == "disabled":
      embed = hikari.Embed(title="Error",
                           description="Target Disabled.",
                           color=embedColors.red)
      embed.add_field("Error:", "creamCoin.disabled error")
      await ctx.respond(embed)
  if interaction == True:

      embed = hikari.Embed(title="Success!",
                           description="set coins successfully ")
      if ctx.options.log:
          logmessage = hikari.Embed(title="Transaction Made",
                                    description="Admin action on " +
                                    ctx.options.user.mention,
                                    color=embedColors.green)
          logmessage.add_field("Set:", str(amount) + " cream coins")
          await logMessage(logmessage)

      await ctx.respond(embed)


@bot.command
@lightbulb.option("disabled",
                  "TRUE OR FALSE",
                  type=hikari.OptionType.BOOLEAN,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.option("user",
                  "the user",
                  type=hikari.OptionType.USER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.command("setdisabled", "disable or enable a user", ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def setdisabled(ctx):
  user = str(ctx.author.id)
  guild = str(ctx.guild_id)
  target = str(ctx.options.user.id)
  #targetmention = ctx.options.user
  disabled = ctx.options.disabled
  interaction = cc.setDisabled(guild, target, disabled, user)
  if interaction == "noperms":
      embed = hikari.Embed(title="Error",
                           description="You are not admin.",
                           color=embedColors.red)
      embed.add_field("Error:", "creamCoin.noperms error")
      await ctx.respond(embed)
  if interaction == "targetnotfound":
      embed = hikari.Embed(title="Error",
                           description="Target Not Found.",
                           color=embedColors.red)
      embed.add_field("Error:", "creamCoin.targetnotfound error")
      await ctx.respond(embed)
  if interaction == "disabled":
      embed = hikari.Embed(title="Error",
                           description="Target Disabled.",
                           color=embedColors.red)
      embed.add_field("Error:", "creamCoin.disabled error")
      await ctx.respond(embed)
  if interaction == True:
      embed = hikari.Embed(title="Success!",
                           description="User [disabled] now set to " +
                           str(disabled),
                           color=embedColors.green)
      await ctx.respond(embed)


@bot.command
@lightbulb.option("amount",
                  "amount of coins to add",
                  type=hikari.OptionType.INTEGER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.option("user",
                  "the user ",
                  type=hikari.OptionType.USER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.command("addcoins", "add coins to a user", ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def addcoins(ctx):
  amount = str(ctx.options.amount)
  target = str(ctx.options.user.id)
  guild = str(ctx.guild_id)
  author = str(ctx.author.id)
  balance = cc.seeCoins(guild, target)
  if balance == "targetnotfound":
      embed = hikari.Embed(title="Error",
                           description="Target Not Found.",
                           color=embedColors.red)
      embed.add_field("Error:", "creamCoin.targetnotfound error")
      await ctx.respond(embed)
  else:
      amounttoset = int(balance) + int(amount)
      interaction = cc.setCoins(guild, target, amounttoset, author)
      embed = hikari.Embed(title="Success!",
                           description=amount +
                           " funds transferred successfully",
                           color=embedColors.green)
      embed.add_field("current funds: ", amounttoset)
      await ctx.respond(embed)


## USER COMMANDS


@bot.command
@lightbulb.add_checks(lightbulb.checks.human_only)
@lightbulb.option("amount",
                  "amount to set coins to",
                  type=hikari.OptionType.INTEGER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.option("user",
                  "the user ",
                  type=hikari.OptionType.USER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.command("transfer", "transfer coins to a user", ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def transfer(ctx):
  randC = randomColor()
  amount = ctx.options.amount
  target = str(ctx.options.user.id)
  guild = str(ctx.guild_id)
  author = str(ctx.author.id)
  if amount < 0:  #user is trying to transfer 0 or less coins
      embed = hikari.Embed(title="Transfer Error",
                           description="",
                           color=embedColors.red)
      embed.add_field("Transfer Error:",
                      "You can't transfer less than 0 coins!")
      embed.set_footer("Run by " + str(ctx.author))
      await ctx.respond(embed)
  interaction = cc.transfer(author, amount, guild, target)
  if interaction == "usernotfound":
      embed = hikari.Embed(title="Error",
                           description="Your Account Not Found.",
                           color=embedColors.red)
      embed.add_field("Error:", "creamCoin.usernotfound error")
      await ctx.respond(embed)
  if interaction == "insfunds":
      embed = hikari.Embed(title="Error",
                           description="Insufficient Funds.",
                           color=embedColors.red)
      embed.add_field("Error:", "creamCoin.insfunds error")
      await ctx.respond(embed)
  if interaction == "guildnotfound":
      embed = hikari.Embed(title="Error",
                           description="Guild Not Found.",
                           color=embedColors.red)
      embed.add_field("Error:", "creamCoin.guildnotfound error")
      await ctx.respond(embed)
  if interaction == True:
      embed = hikari.Embed(title="Success!",
                           description="funds transferred successfully",
                           color=embedColors.green)
      logmessage = hikari.Embed(title="Transaction Made",
                                color=embedColors.green,
                                description="Transaction between " +
                                ctx.author.mention + " -> " +
                                ctx.options.user.mention)
      logmessage.add_field("Transferred:", str(amount) + " cream coins")
      await logMessage(logmessage)
      await ctx.respond(embed)


@bot.command
@lightbulb.add_checks(lightbulb.checks.human_only)
@lightbulb.option("user",
                  "the user to see coin balance",
                  type=hikari.OptionType.USER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=False)
@lightbulb.command("seecoins", "see a user's coins", ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def seecoins(ctx):
  guild = str(ctx.guild_id)
  author = str(ctx.author.id)

  try:
      target = str(ctx.options.user.id)
      targetmention = ctx.target.mention
  except:
      target = author
      targetmention = ctx.author.mention
  interaction = cc.seeCoins(guild, target)

  if interaction == "targetnotfound":
      embed = hikari.Embed(title="Error",
                           description="Target Not Found.",
                           color=embedColors.red)
      embed.add_field("Error:", "creamCoin.targetnotfound error")
      await ctx.respond(embed)
  else:
      embed = hikari.Embed(title="Balance",
                           description="Balance of " + targetmention,
                           color=randomColor())
      embed.add_field("Balance: ", str(interaction))
      await ctx.respond(embed)


##################### END CREAMCOIN COMMANDS #####################

# -- Run Bot -- #

#start web server
keep_alive.keep_alive()

try:
  bot.run()
except:
  os.system("kill 1")