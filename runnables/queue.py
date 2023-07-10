import math
import discord
import playerManager


class QueueView(discord.ui.View):
    current_page: int = 1
    sep: int = 8
    data = []

    async def send(self, interaction):
        self.data = [(url, title, duration, user, str(i+1))
                     for i, (url, title, duration, user) in enumerate(playerManager.queue)]
        self.message = await interaction.response.defer()
        self.message = await interaction.followup.send(view=self)
        await self.update_message(self.data[:self.sep])

    def create_embed(self, data):
        embed = discord.Embed(
            title=f'🎶 Queue 🎶',
            color=discord.Colour.green()
        )
        for item in data:
            embed.add_field(
                name=f'**{item[4]})** {item[1]}',
                value=f'({item[2]}) - Added by {item[3]}',
                inline=False
            ),
        embed.set_footer(
            text=f'Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')
        return embed

    async def update_message(self, data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.grey
            self.prev_button.style = discord.ButtonStyle.grey
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.primary
            self.prev_button.style = discord.ButtonStyle.primary

        if self.current_page == math.ceil(len(self.data) / self.sep):
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.next_button.style = discord.ButtonStyle.grey
            self.last_page_button.style = discord.ButtonStyle.grey
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.next_button.style = discord.ButtonStyle.primary
            self.last_page_button.style = discord.ButtonStyle.primary

    def get_current_page_data(self):
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        if self.current_page == 1:
            from_item = 0
            until_item = self.sep
        if self.current_page == math.ceil(len(self.data) / self.sep):
            from_item = self.current_page * self.sep - self.sep
            until_item = len(self.data)
        return self.data[from_item:until_item]

    @discord.ui.button(label="|<", style=discord.ButtonStyle.primary)
    async def first_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">|", style=discord.ButtonStyle.primary)
    async def last_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = math.ceil(len(self.data) / self.sep)
        await self.update_message(self.get_current_page_data())


def command(bot):
    @bot.tree.command(name="queue", description="Show the queue")
    async def run(interaction: discord.Interaction):
        if not playerManager.queue:
            await interaction.response.send_message("The queue is currently empty.")
        else:
            await QueueView(timeout=None).send(interaction)
