"""
Discord bot for GBF crew Luminosity. Author: Anton#9396
Parts of code borrowed from Krypton's bot template: https://github.com/kkrypt0nn
"""

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType, TextInputStyle
from disnake.ext import commands
from util import db

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
    async def profile(self, interaction, user=None):
        """
        """
        if not user:
            user = interaction.author
        
        nick = user.nick or user.name
        discord_id = user.id

        # Retrieve profile if it exists

        conn = db.connect()
        profile = db.get_profile(discord_id)
        gbf_id = None 

        # If it does not exist, create a new profile
        # If the user called the command for their own profile, also ask for their GBF ID

        if not profile:
            if user == interaction.author:
                interaction.send(embed=embed, components=)

            profile = db.create_profile(discord_id, nick, gbf_id=gbf_id)

        embed = disnake.Embed(
            title=f'**Profile of {user.name}**',
            description=f'Test',
            color=0x74daff
        )

        await interaction.send(embed=embed)

def setup(bot):
    bot.add_cog(Profile(bot))
