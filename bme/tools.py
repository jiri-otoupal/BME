import re
from pathlib import Path
from typing import Optional

import rich
from InquirerPy import inquirer

from bme.saved_types.bookmark import Bookmark
from bme.convertor import get_cmd_str


def highlight(full_str: str, sub_str: Optional[str], color: str):
    f_list = list(full_str)
    if sub_str:
        f_list.insert(full_str.index(sub_str), f"[{color}]")
        f_list.insert(full_str.index(sub_str) + len(sub_str) + 1, f"[/{color}]")
    return "".join(f_list)


def highlight_regex(full_str: str, regex_str: Optional[str], color: str):
    f_list = list(full_str)
    if regex_str:
        for m in re.finditer(regex_str, full_str):
            start, end = (m.start(0), m.end(0))
            f_list.insert(start, f"[{color}]")
            f_list.insert(end + 1, f"[/{color}]")
    return "".join(f_list)


def browse_bookmarks(bookmarks, cmd_str, found, full_word_match, match_case, regex,
                     searched, root_key=None):
    if root_key:
        tmp_bookmarks = bookmarks[root_key]["cmds"]
    else:
        tmp_bookmarks = bookmarks["cmds"]

    for bookmark in tmp_bookmarks:
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


def prepare_cmd_str(match_case, searched, location: Path):
    if searched is None:
        searched = []
    if match_case:
        cmd_str = get_cmd_str(searched)
    else:
        cmd_str = get_cmd_str(searched).lower()
    bookmarks = Bookmark.load_all(location)
    found = set()
    return bookmarks, cmd_str, found


def process_found_n_remove(found, location, root_key=None):
    if found is None or not len(found):
        rich.print("[red]No Commands found[/red]")
        return
    if len(found) > 1:
        chosen = inquirer.select("Select cmd to remove:", found).execute()
    else:
        chosen = found.pop()
    if inquirer.confirm(f"Do you really want to delete command: '{chosen}'").execute():
        Bookmark.remove(chosen, location, root_key=root_key)
    else:
        rich.print("Nothing removed")
        return
    if chosen not in Bookmark.load_all(location):
        rich.print(f"[green]Removed '{chosen}' Successfully[/green]")
    else:
        rich.print(f"[red]Failed to remove '{chosen}'[/red]")
