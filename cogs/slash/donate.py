"""
Discord bot for GBF crew Luminosity. Author: Anton#9396
Parts of code borrowed from Krypton's bot template: https://github.com/kkrypt0nn
"""

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
from enum import Enum
from utils import db

MATERIALS = list(db.read_materials().keys())

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
                name='material',
                description='The material you donated.',
                type=OptionType.string,
                required=True
            )
        ]
    )
    #@checks.not_blacklisted()
    @commands.check(commands.has_role('Crew'))
    async def donate(self, interaction, quantity: commands.Range[1, ...], material):
        """
        """
        user = interaction.user 

        if material.lower() in (mat.lower() for mat in MATERIALS):
            idx = [mat.lower() for mat in MATERIALS].index(material.lower())
            variable = material.strip().lower().replace("'", '').replace('-', ' ').replace(' ', '_')
            conn = db.connect()
            tot = db.save_donation(conn, user.id, variable, quantity)

            embed = disnake.Embed(
                title=f'**{interaction.author.nick or interaction.author.name} donated:**',
                description=f'''{quantity}x {MATERIALS[idx]}

                {user.nick or user.name} has donated a total of **{tot[0]}x** {MATERIALS[idx]}''',
                color=0x74daff
            )
            await interaction.send(embed=embed)
            return 

        embed = disnake.Embed(
            title=f'**Error!**',
            description=f'Could not find a material called {material}',
            color=0xd10000
        )
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Donate(bot))
