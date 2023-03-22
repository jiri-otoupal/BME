from bme.config_mng import Config
from bme.saved_types.bookmark import Bookmark
from bme.saved_types.sequence import Sequence


def init_all():
    Bookmark.init()
    Sequence.init()
    Config.init()
    Config.fix_integrity()
