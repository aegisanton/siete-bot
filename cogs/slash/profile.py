"""
Discord bot for GBF crew Luminosity. Author: Anton#9396
Parts of code borrowed from Krypton's bot template: https://github.com/kkrypt0nn
"""

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands

class Profile(commands.Cog, name='profile-slash'):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='profile',
        description='Checks the profile of a crew member and create one if they do not have one.',
        options=[
            Option(
                name='user',
                description='The crew member whose profile you want to retrieve.',
                type=OptionType.user,
                required=False
            )
        ]
    )
    @commands.check(commands.has_role('Crew'))
    async def profile(self, interaction, user):
        """
        """
        embed = disnake.Embed(
            title=f'**Profile of {user.name}**',
            description=f'Test',
            color=0x74daff
        )

        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Profile(bot))
