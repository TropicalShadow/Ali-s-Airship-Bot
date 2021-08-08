from discord.ext.commands import Bot
from discord.ext.tasks import loop
from enum import Enum, auto
import aiohttp
import json


class PermissionLevel(Enum):
    MEMBER = auto()
    STAFF = auto()
    ADMIN = auto()

class Guild:
    staff_role_id:int = 874048027638239313
    admin_role_id:int = 874048877605552128
    member_role_id:int = 874028391362363422

class AliBot(Bot):
    Tick = "\u2705"
    Cross = "\u274C"
    guild = Guild()