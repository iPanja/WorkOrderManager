import discord
from discord.ext import commands
import MySQLdb

class Manager():
    def __init__(self, bot):
        self.bot = bot
        self.conn = MySQLdb.connect(user="root", passwd="root", db="wom", host="localhost", port=3306)
        self.cursor = self.conn.cursor()
    def isInt(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False
    @commands.command(pass_context = True)
    async def order(self, ctx):
        args = (ctx.message.content).split()[1:]
        item = " ".join(args[:-1]).lower()
        amount = args[-1]
        if not self.isInt(amount):
            await self.bot.send_message(ctx.message.channel, "The amount of the order was not found, it is being set to 1 by default")
            item = " ".join(args).lower()
            amount = 1
        else:
            amount = int(amount)

        self.cursor.execute("""SELECT item, amount FROM orders WHERE item = %s""", (item,))
        self.conn.commit()
        rows = self.cursor.fetchall()
        if len(rows) != 0:
            amount += rows[0][1]
            self.cursor.execute("""UPDATE orders SET amount = %s WHERE item = %s""", (amount, item,))
            self.conn.commit()
            await self.bot.send_message(ctx.message.channel, "An order with that name already exists, it has been updated to " + str(amount) + "x (was " + str(rows[0][1]) + ")")
            return

        self.cursor.execute("""INSERT INTO orders (item, amount, creator) VALUES (%s, %s, %s)""", (item, amount, ctx.message.author.name))
        self.conn.commit()

        await self.bot.send_message(ctx.message.channel, "The order has been processed, thank you!")

    @commands.command(pass_context = True)
    async def orderfinish(self, ctx):
        args = (ctx.message.content).split()[1:]
        item = " ".join(args[:-1]).lower()
        amount = args[-1]

        error = ""
        if not self.isInt(amount):
            print('check')
            error =  "The amount of the order was not found, it is being set to 1 by default.\n"
            item = " ".join(args).lower()
            amount = 1
        else:
            amount = int(amount)
        self.cursor.execute("""SELECT item, amount FROM orders WHERE item = %s""", (item,))
        self.conn.commit()
        results = self.cursor.fetchone()

        if results == None:
            await self.bot.send_message(ctx.message.channel, "The product has not been found, please use the following command to view all current orders. `!orderlist`")
            return

        msg = "You created too many products, but it will still be marked as completed."
        if (results[1] - amount) == 0:
            msg = "Order fulfilled. It has been removed, thank you!"
        if (results[1] - amount) <= 0:
            self.cursor.execute("""DELETE FROM orders WHERE item = %s AND amount = %s""", (item, results[1],))
            self.conn.commit()
            await self.bot.send_message(ctx.message.channel, error + msg)
            return

        amount = results[1] - amount
        self.cursor.execute("""UPDATE orders SET amount = %s WHERE item = %s""", (amount, item,))
        self.conn.commit()
        await self.bot.send_message(ctx.message.channel, error + "Your contributions have been accounted for, thank you! Only " + str(amount) + "x more " + item + "s are needed!")

    @commands.command(pass_context = True)
    async def orderlist(self, ctx):
        msg = "Order List:\n"

        self.cursor.execute("""SELECT item, amount FROM orders""")
        self.conn.commit()
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            await self.bot.send_message(ctx.message.author, "The order list is currently empty.")
            return

        for entry in rows:
            msg += "\t" + str(entry[1]) + "x " + entry[0] + "\n"

        await self.bot.send_message(ctx.message.author, msg)

def setup(bot):
    try:
        bot.add_cog(Manager(bot))
        print("[Manager Module Loaded]")
    except Exception as e:
        print(" >> Manager Module: {0}".format(e))