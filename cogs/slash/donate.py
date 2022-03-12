"""
Discord bot for GBF crew Luminosity. Author: Anton#9396
Parts of code borrowed from Krypton's bot template: https://github.com/kkrypt0nn
"""

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
from enum import Enum

class Centrum(str, Enum):
    Wind_cent = 'Galbinus Centrum'
    Fire_cent = 'Rubeus Centrum'
    Water_cent = 'Indicus Centrum'
    Earth_cent = 'Luteus Centrum'
    Light_cent = 'Niveus Centrum'
    Dark_cent = 'Ater Centrum'

class Scale(str, Enum):
    Wind_scale = 'Green Dragon Scale'
    Fire_scale = 'Red Dragon Scale'
    Water_scale = 'Blue Dragon Scale'
    Earth_scale = 'Brown Dragon Scale'
    Light_scale = 'White Dragon Scale'
    Dark_scale = 'Black Dragon Scale'

class Book(str, Enum):
    Wind_whorl = 'Tempest Whorl'
    Fire_whorl = 'Infernal Whorl'
    Water_whorl = 'Tidal Whorl'
    Earth_whorl = 'Seismic Whorl'
    Light_whorl = 'Radiant Whorl'
    Dark_whorl = 'Umbral Whorl'

class M1(str, Enum):
    Tia_ani = 'Tiamat Anima'
    Tia_o_ani = 'Tiamat Omega Anima'
    Colo_ani = 'Colossus Anima'
    Colo_o_ani = 'Colossus Omega Anima'
    Levi_ani = 'Leviathan Anima'
    Levi_o_ani = 'Leviathan Omega Anima'
    Ygg_ani = 'Yggdrasil Anima'
    Ygg_o_ani = 'Yggdrasil Omega Anima'
    Lumi_ani = 'Luminiera Anima'
    Lumi_o_ani = 'Luminiera Omega Anima'
    Cele_ani = 'Celeste Anima'
    Cele_o_ani = 'Celeste Omega Anima'
    
    Tia_mat = 'Green Dragon Eye'
    Colo_mat = 'Resolute Reactor'
    Levi_mat = 'Fanned Fin'
    Ygg_mat = 'Genesis Bud'
    Lumi_mat = 'Primal Bit'
    Cele_mat = 'Black Fog Sphere'

    Wind_ani = 'True Wind Anima'
    Fire_ani = 'True Fire Anima'
    Water_ani = 'True Water Anima'
    Earth_ani = 'True Earth Anima'
    Light_ani = 'True Light Anima'
    Dark_ani = 'True Dark Anima'

class T1(str, Enum):
    Nez_ani = 'Nezha Anima'
    Nez_o_ani = 'Nezha Omega Anima'
    Te_ani = 'Twin Elements Anima'
    Te_o_ani = 'Twin Elements Omega Anima'
    Mac_ani = 'Macula Marius Anima'
    Mac_o_ani = 'Macula Marius Omega Anima'
    Med_ani = 'Medusa Anima'
    Med_o_ani = 'Medusa Omega Anima'
    Apo_ani = 'Apollo Anima'
    Apo_o_ani = 'Apollo Omega Anima'
    Dao_ani = 'Dark Angel Olivia Anima'
    Dao_o_ani = 'Dark Angel Olivia Omega Anima'

class T2(str, Enum):
    Gar_ani = 'Garuda Anima'
    At_ani = 'Athena Anima'
    Baa_ani = 'Baal Anima'
    Gran_ani = 'Grani Anima'
    Od_ani = 'Odin Anima'
    Li_ani = 'Lich Anima'

class T3(str, Enum):
    Morr_ani = 'Morrigna Anima'
    Prom_ani = 'Promoetheus Anima'
    Ca_ani = 'Ca Ong Anima'
    Gilg_ani = 'Gilgamesh Anima'
    Hec_ani = 'Hector Anima'
    Anu_ani = 'Anubis Anima'

class Island(str, Enum):
    Satin = 'Satin Feather'
    Zephyr = 'Zephyr Feather'
    Flying = 'Flying Sprout'
    Fine = 'Fine Sand Bottle'
    Untamed = 'Untamed Flame'
    Blistering = 'Blistering Ore'
    Fresh = 'Fresh Water Jug'
    Soothing = 'Soothing Splash'
    Glowing = 'Glowing Coral'
    Rough = 'Rough Stone'
    Coarse = 'Coarse Alluvium'
    Swirling = 'Swirling Amber'
    Falcon = 'Falcon Feather'
    Spring = 'Spring Water Jug'
    Vermillion = 'Vermillion Stone'
    Slimy = 'Slimy Shroom'
    Hollow = 'Hollow Soul'
    Lacrimosa = 'Lacrimosa'
    Wheat = 'Wheat Stalk'
    Iron = 'Iron Cluster'
    Olea = 'Olea Plant'
    Indigo = 'Indigo Fruit'
    Foreboding = 'Foreboding Clover'
    Blood = 'Blood Amber'
    Sand = 'Sand Brick'
    Native = 'Native Reed'
    Antique = 'Antique Cloth'
    Prosperity = 'Prosperity Flame'
    Explosive = 'Explosive Material'
    Steel = 'Steel Liquid'
    Dydroit = 'Dydroit Stone'
    Skyrock = 'Skyrock Blossom'
    Affinity = 'Affinity Seed'
    Firn = 'Firn'
    Frozen = 'Frozen Foliole'
    Cold = 'Cold Mold'
    Merkmal = 'Merkmal Fig'
    Bastion = 'Bastion Block'
    Corroded = 'Corroded Cartridge'
    Riot = 'Riot'
    Basii = 'Basii Fruit'
    Raw = 'Raw Gemstone'

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
