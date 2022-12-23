import re

import rich

from bme.bookmark import Bookmark
from bme.convertor import get_cmd_str


def browse_bookmarks(bookmarks, cmd_str, found, full_word_match, match_case, regex,
                     searched):
    for bookmark in bookmarks["cmds"]:
        if match_case:
            b_tmp = bookmark
        else:
            b_tmp = bookmark.lower()

        try:
            if regex is None and (len(set(searched).intersection(
                    b_tmp.split(" "))) or (not full_word_match and cmd_str in b_tmp)):
                found.add(bookmark)
            elif regex and re.findall(regex, b_tmp):
                found.add(bookmark)
        except re.error as ex:
            rich.print(f"[red]Regex Error: {ex.msg}, stopping[/red]")
            return None
    return found


def prepare_cmd_str(match_case, searched):
    if match_case:
        cmd_str = get_cmd_str(searched)
    else:
        cmd_str = get_cmd_str(searched).lower()
    bookmarks = Bookmark.load_all()
    found = set()
    return bookmarks, cmd_str, found
