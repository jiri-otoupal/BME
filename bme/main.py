import click
import rich
from InquirerPy import inquirer
from bme.__version__ import __version_name__, __version__
from bme.config import default_sequences_location, default_bookmarks_location
from bme.daemon.daemon import Daemon


@click.group()
@click.version_option(f"{__version__} {__version_name__}")
def cli():
    """
    BME is productivity tool that will allow you bookmark and make sequences of
    your favourite commands, so you don't have to create scripts and edit your .bashrc
    """
    pass


@cli.group()
def seq():
    """
    This is group for running sequential commands
    """
    pass


@seq.command("create", help="Adds Bookmark, use of quotes is optional",
             context_settings=dict(ignore_unknown_options=True))
@click.argument("name", type=str)
def create_seq(name):
    """
    Creates Sequence

    Example:

    bme sequence create my_sequence

    @param name: Name of sequence to create
    @return:
    """
    from bme.saved_types.sequence import Sequence
    if Sequence.create(name):
        rich.print(
            f"[green]Added New Sequence: '[white]{name}[/white]'[/green]")
    else:
        rich.print(f"[red]Sequence '[white]{name}[/white]' is duplicate, nothing "
                   f"changed[/red]")


@seq.command("rm", help="Adds Bookmark, use of quotes is optional",
             context_settings=dict(ignore_unknown_options=True))
@click.argument("name", type=str)
def remove_seq(name):
    """
    Removes Sequence

    Example:

    bme sequence rm my_sequence

    @param name: Name of sequence to create
    @return:
    """
    from bme.saved_types.sequence import Sequence
    if inquirer.confirm(
            f"Do you really want to remove sequence '{name}'?").execute():
        if Sequence.remove(name):
            rich.print(
                f"[green]Removed Sequence: '[white]{name}[/white]'[/green]")
        else:
            rich.print(f"[red]Sequence '[white]{name}[/white]' does not exist, nothing "
                       f"changed[/red]")
    else:
        rich.print("Canceled")


@seq.command("list", help="Lists commands")
@click.argument("sequence_name", required=False, type=str)
@click.argument("searched", required=False, default=None)
@click.option("-r", "--regex", help="Regex string to check with, please use quotes",
              required=False,
              default=None)
@click.option("-w", "--full-word-match", help="Only full word matching", default=False,
              is_flag=True)
@click.option("-m", "--match-case", help="Match Case", default=False, is_flag=True)
def seq_cmd_list(sequence_name, searched, regex, full_word_match, match_case):
    """
    This will list commands and sequences, if argument is used search in text is applied to results

    Optional flags:

    "-r <your-regex>" or "--regex <your-regex>"` for full word search only
    "-f" or "--full-word" for full word search only
    "-m" or "--match-case" for search with matching case

    Example:

    In sequence DB there is:
     'ssh jiri@192.168.1.0' command
     'ssh jiri@192.168.1.55' command
     'scp jiri@192.168.1.55' command

    bme sequence list

    Will list all the sequences and their commands

    bme sequence list <optional commands that match this to list>

    bme sequence list ssh

    Output:
        'ssh jiri@192.168.1.0' command
        'ssh jiri@192.168.1.55' command


    @param sequence_name: Name of sequence to search
    @param searched: Searched text in commands
    @param regex: Regex string to use to filter, can not be used together with argument
    @param full_word_match: If match only full words
    @param match_case: If false(default) no case is considered during search
    @return:
    """
    from bme.saved_types.sequence import Sequence
    if sequence_name:
        sequences = (sequence_name,)
    else:
        sequences = Sequence.load_all(default_sequences_location).keys()

    if sequence_name is not None and sequence_name not in (sequences := Sequence.load_all(
            default_sequences_location).keys()):
        rich.print(
            f"[red]Did not found searched sequence '[white]{sequence_name}[/white]'.[/red]")
        if len(sequences):
            sequences = (inquirer.select("Please select sequence", sequences).execute(),)
        else:
            rich.print("No sequences in DB")

    for seq in sequences:
        if searched is not None or regex is not None:

            from bme.tools import prepare_cmd_str
            bookmarks, cmd_str, found_cmds = prepare_cmd_str(match_case, searched,
                                                             default_sequences_location)

            from bme.tools import browse_bookmarks
            found_cmds = browse_bookmarks(bookmarks, cmd_str, found_cmds, full_word_match,
                                          match_case,
                                          regex,
                                          searched, sequence_name)
            if found_cmds is None:
                return

        else:
            from bme.saved_types.bookmark import Bookmark
            found_cmds = Bookmark.load_all(default_sequences_location)[seq]["cmds"]

        rich.print(f"[white]Sequence: [green]'{seq}'[/green][/white]")
        if not len(found_cmds):
            rich.print("\t[red]No Commands found[/red]")
            return

        rich.print("\t[bold]Commands:[/bold]")
        for found_cmd in found_cmds:
            if not regex:
                from bme.tools import highlight
                rich.print(f'\t\t{highlight(found_cmd, searched, "red")}')
            else:
                from bme.tools import highlight_regex
                rich.print(f'\t\t{highlight_regex(found_cmd, regex, "red")}')


@seq.command("edit",
             help="Will redirect you to edit file when you can edit sequences",
             context_settings=dict(ignore_unknown_options=True))
def sequence_edit():
    """
    Adds command supplied in argument from sequence

    Example:

    bme sequence edit

    @return:
    """
    rich.print(
        f"[white]Please edit sequences in '[green]{default_sequences_location.absolute()}[/green]'")


@seq.command("add",
             help="Adds Command to sequence, use of quotes is optional",
             context_settings=dict(ignore_unknown_options=True))
@click.argument("sequence_name", type=str)
@click.argument("command", nargs=-1, type=click.UNPROCESSED)
def sequence_add(sequence_name, command):
    """
    Adds command supplied in argument from sequence

    Example:

    bme sequence add my_sequence ssh jiri@192.168.1.0

    @param sequence_name: Name of sequence
    @param command: Command to add, use quotes around command optionally
    @return:
    """
    if not command:
        rich.print(
            f"[red]Can not add empty command to sequence [/red]'[white]{sequence_name}[/white]'")
        return

    from bme.tools import get_correct_sequence
    sequence_name = get_correct_sequence(sequence_name)
    from bme.convertor import get_cmd_str
    cmd_str = get_cmd_str(command)
    from bme.saved_types.sequence import Sequence
    if Sequence.add_cmd(sequence_name, cmd_str):
        rich.print(
            f"[green]Added New command: '[white]{' '.join(command)}[/white]' to sequence "
            f"'[white]{sequence_name}[/white]"
            f"'[/green]")
    else:
        rich.print(
            f"[red]Command '[white]{cmd_str}[/white]' is duplicate in sequence "
            f"'[white]{sequence_name}[/white]', nothing "
            f"changed[/red]")


@seq.command("pop", help="Adds Command to sequence, use of quotes is optional",
             context_settings=dict(ignore_unknown_options=True))
@click.argument("sequence_name", type=str)
@click.argument("searched", nargs=-1, type=click.UNPROCESSED)
@click.option("-r", "--regex", help="Regex string to check with, please use quotes",
              required=False,
              default=None)
@click.option("-w", "--full-word-match", help="Only full word matching", default=False,
              is_flag=True)
@click.option("-m", "--match-case", help="Match Case", default=False, is_flag=True)
def sequence_pop(sequence_name, searched, regex, full_word_match, match_case):
    """
    Removes command supplied in argument from sequence

    Example:

    bme sequence pop ssh jiri@192.168.1.0

    @return:
    """
    from bme.tools import prepare_cmd_str
    bookmarks, cmd_str, found = prepare_cmd_str(match_case, searched,
                                                default_sequences_location)

    if not searched:
        rich.print(
            f"[red]Can not remove empty command from sequence [/red]'[white]{sequence_name}[/white]'")
        return

    from bme.tools import get_correct_sequence
    sequence_name = get_correct_sequence(sequence_name)

    from bme.tools import browse_bookmarks
    found = browse_bookmarks(bookmarks, cmd_str, found, full_word_match, match_case,
                             regex,
                             searched, sequence_name)

    from bme.tools import process_found_n_remove
    process_found_n_remove(found, default_sequences_location, sequence_name)


@seq.command("watch", help="Adds Command to sequence, use of quotes is optional",
             context_settings=dict(ignore_unknown_options=True))
@click.argument("sequence_name", type=str)
@click.argument("file", type=str)
@click.option("-v", "--verbose", required=False, help="Verbose execution of commands")
def sequence_watch(sequence_name, file, verbose):
    """
    Sequence will watch every time supplied file is modified

    Example:

    bme sequence watch my_sequence file_path

    @param verbose: Verbose mode
    @param file:
    @param sequence_name:
    @return:
    """
    from pathlib import Path
    if not Path(file).exists():
        rich.print(f"File does not exist in path {file}")
        return

    from bme.tools import get_correct_sequence
    sequence_name = get_correct_sequence(sequence_name)
    from bme.saved_types.sequence import Sequence
    callback = lambda: Sequence.execute(sequence_name, verbose=verbose)
    from bme.tools import FileModifiedHandler
    FileModifiedHandler(Path(file).absolute(), callback)


@seq.command("run", help="Adds Command to sequence, use of quotes is optional",
             context_settings=dict(ignore_unknown_options=True))
@click.argument("sequence_name", type=str)
@click.argument("arguments", nargs=-1, type=click.UNPROCESSED, required=False,
                default=None)
@click.option("-v", "--verbose", required=False, help="Verbose execution of commands")
def sequence_run(sequence_name, arguments, verbose):
    """
    Adds command supplied in argument

    Example:

    bme sequence run my_sequence

    @param arguments: Arguments for formatting
    @param sequence_name:
    @param verbose:
    @return:
    """
    from bme.tools import get_correct_sequence
    sequence_name = get_correct_sequence(sequence_name)
    from bme.saved_types.sequence import Sequence
    if Sequence.execute(sequence_name, arguments=arguments, verbose=verbose):
        pass
    else:
        rich.print(
            f"[red]Sequence does not exist '[white]{sequence_name}[/white]', exiting..."
            f"[/red]")


@cli.command("add", help="Adds Bookmark, use of quotes is optional",
             context_settings=dict(ignore_unknown_options=True))
@click.argument("command", nargs=-1, type=click.UNPROCESSED)
def add(command):
    """
    Adds command supplied in argument

    Example:

    bme add ssh jiri@192.168.1.0

    @param command: Command to add, use quotes around command optionally
    @return:
    """
    from bme.saved_types.bookmark import Bookmark
    from bme.convertor import get_cmd_str
    cmd_str = get_cmd_str(command)
    if Bookmark.append(cmd_str):
        rich.print(
            f"[green]Added New Bookmark to command: '[white]{' '.join(command)}[/white]'[/green]")
    else:
        rich.print(f"[red]Bookmark '[white]{cmd_str}[/white]' is duplicate, nothing "
                   f"changed[/red]")


@cli.command("rm", help="Removes Bookmark of argument, use of quotes is optional",
             context_settings=dict(ignore_unknown_options=True))
@click.argument("searched", nargs=-1, type=click.UNPROCESSED)
@click.option("-r", "--regex", help="Regex string to check with, please use quotes",
              required=False,
              default=None)
@click.option("-w", "--full-word-match", help="Only full word matching", default=False,
              is_flag=True)
@click.option("-m", "--match-case", help="Match Case", default=False, is_flag=True)
def rm(searched, regex, full_word_match, match_case):
    """
    Removes command from database, provided command will be searched with arguments / flags


    Example:

    bme rm ssh jiri@192.168.1.0

    Optional flags:

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
    from bme.tools import prepare_cmd_str
    bookmarks, cmd_str, found = prepare_cmd_str(match_case, searched,
                                                default_bookmarks_location)

    from bme.tools import browse_bookmarks
    found = browse_bookmarks(bookmarks, cmd_str, found, full_word_match, match_case,
                             regex,
                             searched)

    from bme.tools import process_found_n_remove
    process_found_n_remove(found, default_bookmarks_location)


@cli.command("run", help="Searches and Runs Bookmark of your selection",
             context_settings=dict(ignore_unknown_options=True))
@click.argument("searched", type=click.UNPROCESSED, required=False,
                default=None)
@click.argument("arguments", nargs=-1, type=click.UNPROCESSED, required=False,
                default=None)
@click.option("-r", "--regex", help="Regex string to check with, please use quotes",
              required=False,
              default=None)
@click.option("-w", "--full-word-match", help="Only full word matching", default=False,
              is_flag=True)
@click.option("-m", "--match-case", help="Match Case", default=False, is_flag=True)
@click.option("-e", "--edit", help="Edit command before execution", default=False,
              is_flag=True)
def run(searched, arguments, regex, full_word_match, match_case, edit):
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

    @param arguments: These arguments will be filled on positions of {} in command,
     dict format is supported, you can use {some_name} but then need to use
     some_name="same_value"
    @param edit: This flag will allow to edit before exec
    @param searched: Searched text in commands
    @param regex: Regex string to use to filter, can not be used together with argument
    @param full_word_match: If match only full words
    @param match_case: If false(default) no case is considered during search
    @return:
    """
    from bme.config_mng import Config
    if searched is None:
        rich.print("[red]Please enter at least one letter for search or use [/red]'bme list'")
        return

    from bme.tools import prepare_cmd_str
    bookmarks, cmd_str, found = prepare_cmd_str(match_case, searched,
                                                default_bookmarks_location)

    from bme.tools import browse_bookmarks
    found = browse_bookmarks(bookmarks, cmd_str, found, full_word_match, match_case,
                             regex,
                             searched)
    if found is None:
        return

    if not len(found):
        rich.print("[red]No Commands found[/red]")
        return
    cfg = Config.read()

    if len(found) > 1 or not cfg["auto-execute"]:
        chosen = inquirer.select("Select cmd to execute:", found).execute()
    else:
        chosen = found.pop()

    if edit:
        chosen = inquirer.text("Edit command before executing: ",
                               default=chosen).execute()
    rich.print(f"[red]Executing [/red][green]{chosen}[/green]")
    from bme.tools import format_command
    final = format_command(arguments, chosen)
    import os
    os.system(final)


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
    if searched is not None or regex is not None:

        from bme.tools import prepare_cmd_str
        bookmarks, cmd_str, found_cmds = prepare_cmd_str(match_case, searched,
                                                         default_bookmarks_location)

        from bme.tools import browse_bookmarks
        found_cmds = browse_bookmarks(bookmarks, cmd_str, found_cmds, full_word_match,
                                      match_case,
                                      regex,
                                      searched)
        if found_cmds is None:
            return

    else:
        from bme.saved_types.bookmark import Bookmark
        found_cmds = Bookmark.load_all(default_bookmarks_location)["cmds"]

    if not len(found_cmds):
        rich.print("[red]No Commands found[/red]")
        return

    rich.print("[bold]Commands:[/bold]")
    for found_cmd in found_cmds:
        if not regex:
            from bme.tools import highlight
            rich.print(highlight(found_cmd, searched, "red"))
        else:
            from bme.tools import highlight_regex
            rich.print(highlight_regex(found_cmd, regex, "red"))


@cli.group()
def daemon():
    pass


@daemon.command()
def start():
    rich.print("Starting BME Daemon")
    Daemon.start()


@cli.command("use", help="Switch Bookmark location")
@click.argument("name", required=True)
def use():
    pass


def main():
    from bme.config_mng import Config
    cfg = Config.read()
    if cfg.get("notify-update", True):
        from bme.notifier.version_notifier import Notifier
        Notifier.notify()
    from bme.init import init_all
    init_all()

    cli()


if __name__ == '__main__':
    main()
