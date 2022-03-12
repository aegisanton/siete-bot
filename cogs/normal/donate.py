"""
Discord bot for GBF crew Luminosity. Author: Anton#9396
Parts of code borrowed from Krypton's bot template: https://github.com/kkrypt0nn
"""

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands

class Donate(commands.Cog, name='donate-normal'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='donate',
        description='placeholder',
        options=[
            Option(
                name='quantity',
                description='The quantity you donated.',
                type=OptionType.integer,
                required=True
            ),
            Option(
                name='item',
                description='The item you donated.',
                type=OptionType.string,
                required=True
            )
        ]
    )
    #@checks.not_blacklisted()
    async def donate(self, interaction, quantity, item):
        """
        """

        embed = disnake.Embed(
            title=f'**{interaction.author.name} donated:**',
            description=f'{quantity}x {item}',
            color=0x74daff
        )
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Donate(bot))
