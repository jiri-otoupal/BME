import os
import re

import click
import rich
from InquirerPy import inquirer

from bme.__version__ import __version_name__, __version__
from bme.bookmark import Bookmark
from bme.convertor import get_cmd_str
from bme.historitian.historitian import History
from bme.init import init_all
from bme.notifier.version_notifier import Notifier


@click.group()
@click.version_option(f"{__version__} {__version_name__}")
def cli():
    pass


@cli.command("add", help="Adds Bookmark, use of quotes is optional",
             context_settings=dict(ignore_unknown_options=True))
@click.argument("command", nargs=-1)
def add(command):
    cmd_str = get_cmd_str(command)
    if Bookmark.append(cmd_str):
        rich.print(
            f"[green]Added New Bookmark for '[blue]{command[0]}[/blue]'[/green]")
    else:
        rich.print(f"[red]Bookmark '[blue]{cmd_str}[/blue]' is duplicate, nothing "
                   f"changed[/red]")


@cli.command("rm", help="Removes Bookmark of argument, use of quotes is optional",
             context_settings=dict(ignore_unknown_options=True))
@click.argument("command", nargs=-1)
def rm(command):
    cmd_str = get_cmd_str(command)
    if Bookmark.remove(" ".join(command)):
        rich.print(f"[green]Removed Bookmark '[blue]{cmd_str}[/blue]'[/green]")
    else:
        rich.print(
            f"[red]Bookmark '[blue]{cmd_str}[/blue]' not found, nothing changed[/red]")


@cli.command("run", help="Searches and Runs Bookmark of your selection",
             context_settings=dict(ignore_unknown_options=True))
@click.argument("searched", nargs=-1, required=False, default=None)
@click.option("-r", "--regex", help="Regex string to check with, please use quotes",
              required=False,
              default=None)
@click.option("-w", "--full-word-match", help="Only full word matching", default=False,
              is_flag=True)
@click.option("-m", "--match-case", help="Match Case", default=False, is_flag=True)
@click.option("-e", "--edit", help="Edit command before execution", default=False,
              is_flag=True)
def run(searched, regex, full_word_match, match_case, edit):
    bookmarks, cmd_str, found = prepare_cmd_str(match_case, searched)

    found = browse_bookmarks(bookmarks, cmd_str, found, full_word_match, match_case,
                             regex,
                             searched)
    if found is None:
        return

    if not len(found):
        rich.print("[red]No Commands found[/red]")
        return

    if len(found) > 1:
        chosen = inquirer.select("Select cmd to execute:", found).execute()
    else:
        chosen = found.pop()

    if edit:
        chosen = inquirer.text("Edit command before executing: ",
                               default=chosen).execute()
    rich.print(f"[red]Executing [/red][green]{chosen}[/green]")
    os.system(chosen)


@cli.command("list")
@click.argument("searched", required=False, default=None)
@click.option("-r", "--regex", help="Regex string to check with, please use quotes",
              required=False,
              default=None)
@click.option("-w", "--full-word-match", help="Only full word matching", default=False,
              is_flag=True)
@click.option("-m", "--match-case", help="Match Case", default=False, is_flag=True)
def cmd_list(searched, regex, full_word_match, match_case):
    if searched is not None:
        bookmarks, cmd_str, found = prepare_cmd_str(match_case, searched)

        found = browse_bookmarks(bookmarks, cmd_str, found, full_word_match, match_case,
                                 regex,
                                 searched)
        if found is None:
            return

    else:
        found = Bookmark.load_all()["cmds"]

    if not len(found):
        rich.print("[red]No Commands found[/red]")
        return

    rich.print("Commands:")
    rich.print("\n".join(found))


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


def main():
    Notifier.notify()
    init_all()

    cli()


if __name__ == '__main__':
    main()
