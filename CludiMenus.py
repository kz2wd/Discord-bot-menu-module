import discord
import datetime

emote_indicator = [str(i) + '️⃣' for i in range(1, 10)]


class BetterMenu:  # better version using embeds
    def __init__(self, choice, allowed_id, channel, title="Menu", description="Faites votre choix", color=0x008000,
                 number_of_response=1, active_state=0):
        self.title = title
        self.description = description
        self.color = color
        self.choice = choice  # list of all choice
        self.allowed_id = allowed_id  # list of all player(s)'s id allowed to answer
        self.channel = channel
        self.number_of_response = number_of_response
        self.result_list = []

        # native answer is -1
        for i in range(len(self.allowed_id)):
            self.result_list.append([i])
            for j in range(self.number_of_response):
                self.result_list[i].append(-1)
        self.active_state = active_state

    async def display(self):
        embed = EmbedCreator(self.title, self.description, self.choice, self.color).embed_message
        x = await self.channel.send(content=None, embed=embed)

        for i in range(len(self.choice)):
            await x.add_reaction(emote_indicator[i])

    def menu_is_answered(self):
        everybody_answered = True
        for allowed_id in self.result_list:
            for answer in range(self.number_of_response):
                if allowed_id[answer + 1] == -1:
                    everybody_answered = False

        return everybody_answered


class EmbedCreator:
    def __init__(self, title, description, choices, color, date=datetime.datetime.utcnow(), footer="React to select"):
        self.embed_message = discord.Embed(title=title, description=description, color=color,
                                           timestamp=date)
        for counter, item in enumerate(choices):
            self.embed_message.add_field(name=item, value=str(counter + 1), inline=True)

        self.embed_message.set_footer(text=footer)


class MenuHandler:  # a way to manage menus
    def __init__(self):
        self.menu_list = []
        self.state = 0  # you can change this to activate or deactivate menus

    def on_reaction_add_menu(self, reaction, user):
        for h in self.menu_list:
            if self.state == h.active_state:
                for i, item_id in enumerate(h.allowed_id):
                    if user.id == item_id:
                        for j, item in enumerate(emote_indicator):
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
                        for j, item in enumerate(emote_indicator):
                            if item == reaction.emoji:
                                for k in range(h.number_of_response):
                                    if h.result_list[i][k + 1] == j:
                                        h.result_list[i][k + 1] = -1
