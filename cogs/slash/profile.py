"""
Discord bot for GBF crew Luminosity. Author: Anton#9396
Parts of code borrowed from Krypton's bot template: https://github.com/kkrypt0nn
"""

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType, TextInputStyle
from disnake.ext import commands
from utils import db

FIRE_SUMMONS = ['Agni', 'Colossus Omega', 'Shiva', 'Michael', 'Red Hare', 'Surtr', 'Wilnas', 'Athena (Summer)', 'Satyr (Summer)']
WATER_SUMMONS = ['Varuna', 'Leviathan Omega', 'Europa', 'Gabriel', 'Charybdis', 'Princess Long Ji', 'Bonito', 'Kaguya', 'Macual Marius (Summer)']
WIND_SUMMONS = ['Zephyrus', 'Tiamat Omega', 'Grimnir', 'Raphael', 'Owlcat', 'Elil', 'Ewiyar', 'Demonbream', 'Freyr', 'Rose Queen (Summer)', 'Tiamat (Summer)']
EARTH_SUMMONS = ['Titan', 'Yggdrasil Omega', 'Godsworn Alexiel', 'Uriel', 'Mammoth', 'Dogu', 'Galleon', 'Gorilla', 'Tsuchinoko', 'Freyr (Yukata)', 'Mandrake (Summer)', 'Yggdrasil (Summer)']
LIGHT_SUMMONS = ['Zeus', 'Luminiera Omega', 'Lucifer', 'Metatron', 'Halluel and Malluel', 'Grand Order', 'Artemis', 'Heimdallr', 'Aphrodite', 'Thor', 'Kaguya (Summer)']
DARK_SUMMONS = ['Hades', 'Celeste Omega', 'Bahamut', 'Sariel', 'Belial', 'Beelzebub', 'Zirnitra', 'Nyarlathotep', 'Typhon', 'Sariel (Holiday)']
MISC_SUMMONS = ['Qilin', 'Huanglong', 'White Rabbit', 'Black Rabbit', 'Kaguya', 'Belle Sylphid', 'Nobiyo', 'Belial', 'Beelzebub', 'Cait Sith']

def embed_profile(bot, profile, user, spark=False, summon=False):

    _, gbf_id, _, crystals, tix, ten_tix, rolls, fire_a, fire_b, water_a, water_b, wind_a, wind_b, earth_a, earth_b, light_a, light_b, dark_a, dark_b, misc_a, misc_b = profile

    crystals_emo = bot.get_emoji(952372312546607194)
    tix_emo = bot.get_emoji(952372462304251944)
    ten_emo = bot.get_emoji(952372451633926144)

    if spark:
        progress = round((float(rolls) / 300) * 100, 1)
        metric = 'roll' if rolls == 1 else 'rolls'
        embed = disnake.Embed(
            title=f'**Spark progress for {user.nick or user.name}**',
            description=f'''{crystals_emo} {crystals}
            {tix_emo} {tix}
            {ten_emo} {ten_tix}

            {user.nick or user.name} currently has **{rolls}** {metric} ({progress}% of a spark)
            ''',
            color=0x74daff            
        )
        embed.set_thumbnail(
            url=user.avatar.url
        )

        return embed

    fire_emo = bot.get_emoji(952542716313612398)
    water_emo = bot.get_emoji(952542724790288426)
    wind_emo = bot.get_emoji(952542742477701140)
    earth_emo = bot.get_emoji(952542733787078707)
    light_emo = bot.get_emoji(952542751105376286)
    dark_emo = bot.get_emoji(952542760509014036)

    if summon:
        embed = disnake.Embed(
            title=f'**Support summons set by {user.nick or user.name}**',
            description=f'''{fire_emo} `{fire_a}` `{fire_b}`
            {water_emo} `{water_a}` `{water_b}`
            {wind_emo} `{wind_a}` `{wind_b}`
            {earth_emo} `{earth_a}` `{earth_b}`
            {light_emo} `{light_a}` `{light_b}`
            {dark_emo} `{dark_a}` `{dark_b}`
            `{misc_a}` `{misc_b}`
            ''',
            color=0x74daff  
        )
        embed.set_thumbnail(
            url=user.avatar.url
        )

        return embed

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
        value=f'{crystals_emo} {crystals}'
    )
    embed.add_field(
        name='Draw Tickets',
        value=f'{tix_emo} {tix}'
    )
    embed.add_field(
        name='10-Draw Tickets',
        value=f'{ten_emo} {ten_tix}'
    )
    embed.add_field(
        name='Draws',
        value=rolls
    )
    embed.add_field(
        name='Fire Summons',
        value=f'''{fire_emo} {fire_a}\n
        {fire_emo} {fire_b}
        '''
    )
    embed.add_field(
        name='Water Summons',
        value=f'''{water_emo} {water_a}\n
        {water_emo} {water_b}
        '''
    )
    embed.add_field(
        name='Wind Summons',
        value=f'''{wind_emo} {wind_a}\n
        {wind_emo} {wind_b}
        '''
    )
    embed.add_field(
        name='Earth Summons',
        value=f'''{earth_emo} {earth_a}\n
        {earth_emo} {earth_b}
        '''
    )
    embed.add_field(
        name='Light Summons',
        value=f'''{light_emo} {light_a}\n
        {light_emo} {light_b}
        '''
    )
    embed.add_field(
        name='Dark Summons',
        value=f'''{dark_emo} {dark_a}\n
        {dark_emo} {dark_b}
        '''
    )
    embed.add_field(
        name='Misc Summons',
        value=f'''{misc_a}\n
        {misc_b}
        '''
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

    summon_options = [
        Option(
            name='fire_a',
            description='Fire Support Summon A',
            type=OptionType.string,
            choices=FIRE_SUMMONS,
            required=False
        ),
        Option(
            name='fire_b',
            description='Fire Support Summon B',
            type=OptionType.string,
            choices=FIRE_SUMMONS,
            required=False
        ),
        Option(
            name='water_a',
            description='Water Support Summon A',
            type=OptionType.string,
            choices=WATER_SUMMONS,
            required=False
        ),
        Option(
            name='water_b',
            description='Water Support Summon B',
            type=OptionType.string,
            choices=WATER_SUMMONS,
            required=False
        ),
        Option(
            name='wind_a',
            description='Wind Support Summon A',
            type=OptionType.string,
            choices=WIND_SUMMONS,
            required=False
        ),
        Option(
            name='wind_b',
            description='Wind Support Summon B',
            type=OptionType.string,
            choices=WIND_SUMMONS,
            required=False
        ),    
        Option(
            name='earth_a',
            description='Earth Support Summon A',
            type=OptionType.string,
            choices=EARTH_SUMMONS,
            required=False
        ),
        Option(
            name='earth_b',
            description='Earth Support Summon B',
            type=OptionType.string,
            choices=EARTH_SUMMONS,
            required=False
        ),
        Option(
            name='light_a',
            description='Light Support Summon A',
            type=OptionType.string,
            choices=LIGHT_SUMMONS,
            required=False
        ),
        Option(
            name='light_b',
            description='Light Support Summon B',
            type=OptionType.string,
            choices=LIGHT_SUMMONS,
            required=False
        ),
        Option(
            name='dark_a',
            description='Dark Support Summon A',
            type=OptionType.string,
            choices=DARK_SUMMONS,
            required=False
        ),
        Option(
            name='dark_b',
            description='Dark Support Summon B',
            type=OptionType.string,
            choices=DARK_SUMMONS,
            required=False
        ),
        Option(
            name='misc_a',
            description='Misc Support Summon A',
            type=OptionType.string,
            choices=MISC_SUMMONS,
            required=False
        ),
        Option(
            name='misc_b',
            description='Misc Support Summon B',
            type=OptionType.string,
            choices=MISC_SUMMONS,
            required=False
        ),
    ]

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
                    description=f'Profile for {nick} does not exist!',
                    color=0xd10000
                )

                await interaction.send(embed=embed)
                return

            embed = embed_profile(self.bot, profile, user)

            await interaction.send(embed=embed)
        

    @commands.slash_command(
        name='spark',
        description='Update your spark progress.',
        options=[
            Option(
                name='crystals',
                description='The amount of crystals to set',
                type=OptionType.integer,
                required=False
            ),
            Option(
                name='tickets',
                description='The amount of draw tickets to set',
                type=OptionType.integer,
                required=False
            ),
            Option(
                name='ten_tickets',
                description='The amount of 10-draw tickets to set',
                type=OptionType.integer,
                required=False
            )
        ]
    )
    @commands.check(commands.has_role('Crew'))
    async def spark(self, interaction, **resources):
        """
        """
        user = interaction.user
        nick = user.nick or user.name

        # Retrieve profile if it exists

        conn = db.connect()
        profile = db.get_profile(conn, user.id)

        # If a profile does not exist, exit with an error 
        if not profile:
            embed = disnake.Embed(
                title=f'**Error!**',
                description=f'Please create a profile first!',
                color=0xd10000
            )

            await interaction.send(embed=embed)
            conn.close()
            return

        # Update spark 

        profile = db.update_spark(conn, user.id, resources, profile)
        embed = embed_profile(self.bot, profile, user, spark=True)
        await interaction.send(embed=embed)

    @commands.slash_command(
        name='summons',
        description='Update your support summons.',
        options=summon_options
    )
    @commands.check(commands.has_role('Crew'))
    async def summons(self, interaction, **summons):
        """
        """

        user = interaction.user
        nick = user.nick or user.name

        # Retrieve profile if it exists

        conn = db.connect()
        profile = db.get_profile(conn, user.id)

        # If a profile does not exist, exit with an error 
        if not profile:
            embed = disnake.Embed(
                title=f'**Error!**',
                description=f'Please create a profile first!',
                color=0xd10000
            )

            await interaction.send(embed=embed)
            conn.close()
            return

        # Update support summons

        profile = db.update_summons(conn, user.id, summons)
        conn.close()
        embed = embed_profile(self.bot, profile, user, summon=True)
        await interaction.send(embed=embed)

        
def setup(bot):
    bot.add_cog(Profile(bot))
