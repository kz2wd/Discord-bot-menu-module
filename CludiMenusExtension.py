import discord
import datetime


alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

validation = "`Validate`"

emote_alphabet = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲',
                  '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿']

go_forward = "⏩"


class Menu:  # first version of menu
    def __init__(self, choice, allowed_id, channel, number_of_response, active_state):
        self.choice = choice  # list of all choice
        self.allowed_id = allowed_id  # list of all player(s)'s id allowed to answer
        self.channel = channel
        self.reaction_allowed = True
        self.message_allowed = True
        self.number_of_response = number_of_response
        self.result_list = []
        for i in range(len(self.allowed_id)):
            self.result_list.append([i])
            for j in range(self.number_of_response):
                self.result_list[i].append(-1)
        self.active_state = active_state

    async def display(self):
        x = await self.channel.send((
            "\n".join("`{} : {}`".format(alphabet[i], item) for i, item in enumerate(self.choice))) +
                                "\n```Make your choice```")

        if self.reaction_allowed:
            for i in range(len(self.choice)):
                await x.add_reaction(emote_alphabet[i])

    async def validate(self):
        x = await self.channel.send(validation)
        await x.add_reaction(go_forward)


class SimpleMenu:  # first version of menu
    def __init__(self, emotes, allowed_id, channel, sentence=None, number_of_response=1, active_state=0):
        self.emotes = emotes
        self.allowed_id = allowed_id  # list of all player(s)'s id allowed to answer
        self.channel = channel
        self.number_of_response = number_of_response
        self.result_list = []
        for i in range(len(self.allowed_id)):
            self.result_list.append([i])
            for j in range(self.number_of_response):
                self.result_list[i].append(-1)
        self.active_state = active_state

        if sentence is None:
            self.sentence = "Make your choice"
        else:
            self.sentence = sentence

    async def display(self):
        x = await self.channel.send(self.sentence)

        for i in range(len(self.emotes)):
            await x.add_reaction(self.emotes[i])

    async def validate(self):
        x = await self.channel.send(validation)
        await x.add_reaction(go_forward)

    def menu_is_answered(self):
        everybody_answered = True
        for allowed_id in self.result_list:
            for answer in range(self.number_of_response):
                if allowed_id[answer + 1] == -1:
                    everybody_answered = False

        return everybody_answered


class BetterMenu:  # better version using embeds
    def __init__(self, choice, allowed_id, channel, title="Menu", description="make your choice", color=0x008000,
                 number_of_response=1, active_state=0):
        self.title = title
        self.description = description
        self.color = color
        self.choice = choice  # list of all choice
        self.allowed_id = allowed_id  # list of all player(s)'s id allowed to answer
        self.channel = channel
        self.reaction_allowed = True
        self.message_allowed = True  # not implemented yet
        self.number_of_response = number_of_response
        self.result_list = []
        for i in range(len(self.allowed_id)):
            self.result_list.append([i])
            for j in range(self.number_of_response):
                self.result_list[i].append(-1)
        self.active_state = active_state

    async def display(self):
        embed = EmbedCreator(self.title, self.description, self.choice, self.color).embed_message
        x = await self.channel.send(content=None, embed=embed)

        if self.reaction_allowed:
            for i in range(len(self.choice)):
                await x.add_reaction(emote_alphabet[i])

    async def validate(self):
        x = await self.channel.send(validation)
        await x.add_reaction(go_forward)

    def menu_is_answered(self):
        everybody_answered = True
        for allowed_id in self.result_list:
            for answer in range(self.number_of_response):
                if allowed_id[answer + 1] == -1:
                    everybody_answered = False

        return everybody_answered


class MenuHandler:  # a way to manage menus
    def __init__(self):
        self.menu_list = []
        self.state = 0  # you can change this to activate or deactivate menus

    def on_reaction_add_menu(self, reaction, user):
        for h in self.menu_list:
            if self.state == h.active_state:
                for i, item_id in enumerate(h.allowed_id):
                    if user.id == item_id:
                        for j, item in enumerate(emote_alphabet):
                            if item == reaction.emoji:
                                number_of_response_not_filled = True
                                for k in range(h.number_of_response):
                                    if number_of_response_not_filled:
                                        if h.result_list[i][k + 1] == -1:
                                            h.result_list[i][k + 1] = j
                                            number_of_response_not_filled = False

    def on_reaction_remove_menu(self, reaction, user):
        for h in self.menu_list:
            if self.state == h.active_state:
                for i, item_id in enumerate(h.allowed_id):
                    if user.id == item_id:
                        for j, item in enumerate(emote_alphabet):
                            if item == reaction.emoji:
                                for k in range(h.number_of_response):
                                    if h.result_list[i][k + 1] == j:
                                        h.result_list[i][k + 1] = -1


class SimpleMenuHandler:  # a way to manage simple menus
    def __init__(self):
        self.menu_list = []
        self.state = 0  # you can change this to activate or deactivate menus
        self.emotes = []

    def on_reaction_add_menu(self, reaction, user):
        for h, menu in enumerate(self.menu_list):
            if self.state == menu.active_state:
                for i, item_id in enumerate(menu.allowed_id):
                    if user.id == item_id:
                        for j, item in enumerate(self.emotes[h]):
                            if item == reaction.emoji:
                                number_of_response_not_filled = True
                                for k in range(menu.number_of_response):
                                    if number_of_response_not_filled:
                                        if menu.result_list[i][k + 1] == -1:
                                            menu.result_list[i][k + 1] = j
                                            number_of_response_not_filled = False

    def on_reaction_remove_menu(self, reaction, user):
        for h, menu in enumerate(self.menu_list):
            if self.state == menu.active_state:
                for i, item_id in enumerate(menu.allowed_id):
                    if user.id == item_id:
                        for j, item in enumerate(self.emotes[h]):
                            if item == reaction.emoji:
                                for k in range(menu.number_of_response):
                                    if menu.result_list[i][k + 1] == j:
                                        menu.result_list[i][k + 1] = -1

    def add_simple_menu(self, simple_menu):
        self.menu_list.append(simple_menu)
        self.emotes.append(simple_menu.emotes)


class EmbedCreator:
    def __init__(self, title, description, choices, color, date=datetime.datetime.utcnow(), footer="React to select"):
        self.embed_message = discord.Embed(title=title, description=description, color=color,
                                           timestamp=date)
        for counter, item in enumerate(choices):
            self.embed_message.add_field(name=item, value=str(counter + 1), inline=True)

        self.embed_message.set_footer(text=footer)