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
        for menu in self.menu_list:
            if menu.active_state == self.state:
                for id_counter, id_authorized in enumerate(menu.allowed_id):
                    if id_authorized == user.id:
                        for emote_counter, emote in enumerate(emote_indicator):
                            if emote == reaction.emoji:
                                number_of_response_not_filled = True
                                for k in range(menu.number_of_response):
                                    if number_of_response_not_filled:
                                        if menu.result_list[id_counter][k + 1] == -1:
                                            menu.result_list[id_counter][k + 1] = emote_counter
                                            number_of_response_not_filled = False

    def on_reaction_remove_menu(self, reaction, user):
        for menu in self.menu_list:
            if menu.active_state == self.state:
                for id_counter, id_authorized in enumerate(menu.allowed_id):
                    if id_authorized == user.id:
                        for emote_counter, emote in enumerate(emote_indicator):
                            if emote == reaction.emoji:
                                for k in range(menu.number_of_response):
                                    if menu.result_list[id_counter][k + 1] == emote_counter:
                                        menu.result_list[id_counter][k + 1] = -1
