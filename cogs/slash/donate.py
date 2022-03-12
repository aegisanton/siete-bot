"""
Discord bot for GBF crew Luminosity. Author: Anton#9396
Parts of code borrowed from Krypton's bot template: https://github.com/kkrypt0nn
"""

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands

class Donate(commands.Cog, name='donate-slash'):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='test',
        description='placeholder',
        options=[
            Option(
                name='item',
                description='The item you donated.',
                type=OptionType.string,
                required=True
            )
        ]
    )
    #@checks.not_blacklisted()
    async def test(self, interaction, item):
        """
        """

        embed = disnake.Embed(
            title=f'**{interaction.author} donated:**',
            description=f'{donation}',
            color=0x9C84EF
        )
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Donate(bot))
