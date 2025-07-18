from SUHANIMUSIC.core.bot import SUHANI
from SUHANIMUSIC.core.dir import dirr
from SUHANIMUSIC.core.git import git
from SUHANIMUSIC.core.userbot import Userbot
from SUHANIMUSIC.misc import dbb, heroku

from SafoneAPI import SafoneAPI
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = SUHANI()
api = SafoneAPI()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
