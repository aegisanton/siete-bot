"""
Discord bot for GBF crew Luminosity. Author: Anton#9396
Parts of code borrowed from Krypton's bot template: https://github.com/kkrypt0nn
"""

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType, TextInputStyle
from disnake.ext import commands
from utils import db

def embed_profile(bot, profile, user):
    gbf_id = profile[1]
    crystals = profile[3]
    tix = profile[4]
    ten_tix = profile[5]
    rolls = profile[6]

    crystals_emo = bot.get_emoji(952372312546607194)
    tix_emo = bot.get_emoji(952372462304251944)
    ten_emo = bot.get_emoji(952372451633926144)

    embed = disnake.Embed(
        title=f'**Profile of {user.nick or user.name}**',
        color=0x74daff
    )
    embed.set_thumbnail(
        url=user.avatar.url
    )
    embed.add_field(
        name='GBF ID',
        value=gbf_id
    )
    embed.add_field(
        name='Crystals',
        value=f'{crystals_emo} {crystals}',
        inline=True
    )
    embed.add_field(
        name='Draw Tickets',
        value=f'{tix_emo} {tix}',
        inline=True
    )
    embed.add_field(
        name='10-Draw Tickets',
        value=f'{ten_emo} {ten_tix}',
        inline=True
    )
    embed.add_field(
        name='Draws',
        value=rolls,
        inline=True
    )

    return embed 

class Input(disnake.ui.Modal):
    def __init__(self, interaction, conn, bot):
        super().__init__(
            title='Create Profile',
            custom_id=f'create_profile-{interaction.id}',
            timeout=120,
             components=[
                disnake.ui.TextInput(
                    label='GBF ID',
                    placeholder='000',
                    custom_id=f'gbf_id-{interaction.id}',
                    style=TextInputStyle.short,
                    max_length=20
                )
            ]
        )
        self.conn = conn
        self.interaction= interaction
        self.bot = bot 
    
    async def callback(self, interaction):
        gbf_id = interaction.text_values.get(f'gbf_id-{self.interaction.id}')
        user = self.interaction.user
        profile = db.create_profile(self.conn, user.id, (user.nick or user.name), gbf_id=gbf_id)
        self.conn.close()

        embed = embed_profile(self.bot, profile, user)
        await interaction.response.send_message(embed=embed)

class Profile(commands.Cog, name='profile-slash'):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='profile',
        description='Checks the profile of a crew member or yourself.',
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

        # Retrieve profile if it exists

        conn = db.connect()
        profile = db.get_profile(conn, user.id)
        #conn.close()

        # If it does not exist, create a new profile
        # If the user called the command for their own profile, also ask for their GBF ID

        if not profile and user == interaction.author:
            gbf_id = None 
            await interaction.response.send_modal(modal=Input(interaction, conn, self.bot))
            return
        else:
            if not profile:
                #prof = db.create_profile(conn, user.id, (user.nick or user.name))
                #conn.close()

                embed = disnake.Embed(
                    title=f'**Error!**',
                    description=f'Profile for {nick} does not exist!'
                    color=0xd10000
                )

                await interaction.send(embed=embed)
                return

            embed = embed_profile(self.bot, profile, user)

            await interaction.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Profile(bot))
