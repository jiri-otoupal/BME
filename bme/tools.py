import re

import rich

from bme.bookmark import Bookmark
from bme.convertor import get_cmd_str


def highlight(full_str: str, sub_str: str, color: str):
    f_list = list(full_str)
    f_list.insert(full_str.index(sub_str), f"[{color}]")
    f_list.insert(full_str.index(sub_str) + len(sub_str) + 1, f"[/{color}]")
    return "".join(f_list)


def highlight_regex(full_str: str, regex_str: str, color: str):
    f_list = list(full_str)
    for m in re.finditer(regex_str, full_str):
        start, end = (m.start(0), m.end(0))
        f_list.insert(start, f"[{color}]")
        f_list.insert(end + 1, f"[/{color}]")
    return "".join(f_list)


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
    if searched is None:
        searched = []
    if match_case:
        cmd_str = get_cmd_str(searched)
    else:
        cmd_str = get_cmd_str(searched).lower()
    bookmarks = Bookmark.load_all()
    found = set()
    return bookmarks, cmd_str, found
