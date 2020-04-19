import discord

import CludiMenus


# create a menu handler
my_menu_handler = CludiMenus.MenuHandler()
# menu handler will help you for 2 things

# firstly, it will allow you to get answers from a menu

# Secondly, it will allow you to simply check how many menus you have created
# # if you want to see the answers of a menu but it may not have been created it can cause an error
# # the menu handler will avoid that


class Bot(discord.Client):
    async def on_ready(self):
        print("{}, {}, is ready".format(self.user.name, self.user.id))

    async def on_message(self, message):
        if message.author != self.user:
            print(message.author.name, ":", message)

        elif message.startwith == "menu":

            # mains parameters of BetterMenu class
            choices = ["Hey", "Goodbye"]
            authorized_ids = [message.author.id]
            channel = message.channel
            title = "My menu"
            description = "This is my menu"
            color = 0x008000
            number_of_answer = 1

            # create the BetterMenu
            my_menu_handler.menu_list.append(CludiMenus.BetterMenu(choices, authorized_ids, channel, title, description, color, number_of_answer))

            # display the BetterMenu
            await my_menu_handler.menu_list[0].display()

    async def on_reaction_add(self, reaction, user):
        if user != self.user:
            print(user.name, "reacted with :", reaction)

            # this line allow the menu handler to fill menus with answers
            my_menu_handler.on_reaction_add_menu(reaction, user)
            # you do not need to check 'if user != self.user' if the client is not an the allowed_id list

            # check if a menu is created
            if len(my_menu_handler.menu_list) > 0:
                # check if the menu if fully answered, return True if it is the case so we can continue
                if my_menu_handler.menu_list[0].menu_is_answered():
                    # print the list with all the result
                    print(my_menu_handler.menu_list[0].result_list)
                    # the format of the list is :
                    # [[id_of_an_user, his_first_answer, his_second_answer, 3th, 4th, ...], [2id, 1st answer, ...], ...]
                    # the format of the answer is a number, representing the index of an item in the choices list
                    # in our example, we expect to see something like this :
                    # [[1234567, 1]]
                    # so, to see the answer, we can simply do :
                    index = my_menu_handler.menu_list[0].result_list[0][1]
                    user_choice = my_menu_handler.menu_list[0].choice[index]
                    print(user_choice)

                    # then you can do whatever you want with it

                    await reaction.channel.send("You selected", user_choice)

    async def game_on_reaction_remove(self, reaction, user):
        if user != self.user:
            print(user.name, "removed reaction :", reaction)

            # this line allow the menu handler to replace answer from a menu with -1, if the user want to change his choice
            my_menu_handler.on_reaction_remove_menu(reaction, user)


client = Bot()
token = 'Create a bot on discord to get a token'
client.run(token)
