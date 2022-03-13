"""
Discord bot for GBF crew Luminosity. Author: Anton#9396
Parts of code borrowed from Krypton's bot template: https://github.com/kkrypt0nn
"""

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
from enum import Enum

class Misc(str, Enum):
    Rupie = 'Rupie'
    Champion = 'Champion Merit'
    Supreme = 'Supreme Merit'

class Donate(commands.Cog, name='donate-slash'):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='donate',
        description='Register a donation to the crew island resort.',
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
    async def donate(self, interaction, quantity: commands.Range[1, ...], item):
        """
        """

        embed = disnake.Embed(
            title=f'**{interaction.author.nick or interaction.author.name} donated:**',
            description=f'{quantity}x {item}',
            color=0x74daff
        )
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Donate(bot))
