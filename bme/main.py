import os

import click
import rich
from InquirerPy import inquirer

from bme.__version__ import __version_name__, __version__
from bme.bookmark import Bookmark
from bme.convertor import get_cmd_str
from bme.init import init_all
from bme.notifier.version_notifier import Notifier
from bme.tools import browse_bookmarks, prepare_cmd_str


@click.group()
@click.version_option(f"{__version__} {__version_name__}")
def cli():
    pass


@cli.command("add", help="Adds Bookmark, use of quotes is optional",
             context_settings=dict(ignore_unknown_options=True))
@click.argument("command", nargs=-1)
def add(command):
    """
    Adds command supplied in argument

    Example:

    bme add ssh jiri@192.168.1.0

    @param command: Command to add, use quotes around command optionally
    @return:
    """
    cmd_str = get_cmd_str(command)
    if Bookmark.append(cmd_str):
        rich.print(
            f"[green]Added New Bookmark to command: '[white]{command}[/white]'[/green]")
    else:
        rich.print(f"[red]Bookmark '[white]{cmd_str}[/white]' is duplicate, nothing "
                   f"changed[/red]")


@cli.command("rm", help="Removes Bookmark of argument, use of quotes is optional",
             context_settings=dict(ignore_unknown_options=True))
@click.argument("command", nargs=-1)
def rm(command):
    """
    Removes command from database, provided command needs to be exactly same


    Example:

    bme rm ssh jiri@192.168.1.0

    @param command: Command to add, use quotes around command optionally
    @return:
    """
    cmd_str = get_cmd_str(command)
    if Bookmark.remove(" ".join(command)):
        rich.print(f"[green]Removed Bookmark '[white]{cmd_str}[/white]'[/green]")
    else:
        rich.print(
            f"[red]Bookmark '[white]{cmd_str}[/white]' not found, nothing changed[/red]")


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
    """
    This will run command, argument is used for search in commands for a match

    Optional flags:

    "-e" or "--edit" for editing command before execution
    "-r <your-regex>" or "--regex <your-regex>"` for full word search only
    "-f" or "--full-word" for full word search only
    "-m" or "--match-case" for search with matching case

    Example:

    In DB there is 'ssh jiri@192.168.1.0' command

    Use following to execute command
    bme run ssh or bme run jiri@192 or bme run <whatever matches in command>

    @param searched: Searched text in commands
    @param regex: Regex string to use to filter, can not be used together with argument
    @param full_word_match: If match only full words
    @param match_case: If false(default) no case is considered during search
    @return:
    """
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


@cli.command("list", help="Lists commands")
@click.argument("searched", required=False, default=None)
@click.option("-r", "--regex", help="Regex string to check with, please use quotes",
              required=False,
              default=None)
@click.option("-w", "--full-word-match", help="Only full word matching", default=False,
              is_flag=True)
@click.option("-m", "--match-case", help="Match Case", default=False, is_flag=True)
def cmd_list(searched, regex, full_word_match, match_case):
    """
    This will list commands, if argument is used search in text is applied to results

    Optional flags:

    "-e" or "--edit" for editing command before execution
    "-r <your-regex>" or "--regex <your-regex>"` for full word search only
    "-f" or "--full-word" for full word search only
    "-m" or "--match-case" for search with matching case

    Example:

    In DB there is:
     'ssh jiri@192.168.1.0' command
     'ssh jiri@192.168.1.55' command
     'scp jiri@192.168.1.55' command


    bme list <optional commands that match this to list>

    bme list ssh

    Output:
        'ssh jiri@192.168.1.0' command
        'ssh jiri@192.168.1.55' command


    @param searched: Searched text in commands
    @param regex: Regex string to use to filter, can not be used together with argument
    @param full_word_match: If match only full words
    @param match_case: If false(default) no case is considered during search
    @return:
    """
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


def main():
    Notifier.notify()
    init_all()

    cli()


if __name__ == '__main__':
    main()
