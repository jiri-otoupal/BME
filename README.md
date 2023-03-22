# BME

(Bookmark my Executions/Commands)

Never use notepads or history for searching for your past commands. With BME you can bookmark your commands, search in your bookmarked commands and
execute them with edit possibility before execution.

[![image](https://img.shields.io/pypi/v/bme.svg)](https://pypi.org/project/bme/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bme)](https://pypi.org/project/bme/)
[![Downloads](https://pepy.tech/badge/bme)](https://pepy.tech/project/bme)

### Supported

#### OS

No specific requirements here, whatever runs Python

## Requirements

### Python

* 3.7+

## Installing

### MacOS

On most MacOS machines there is `pip3` instead of `pip` **use pip3 for install**

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

```bash
pip install bme

or

pip3 install bme
```

## All your commands are saved in '~/.bme/bookmarks.json'

## Usage:

#### For adding bookmark:

_(Quotas can be used)_

```
bme add <your command>
```

#### For Removing bookmark:

_(Quotas can be used)_

```
bme rm <your command>
```

#### For List bookmarks:

_(Quotas can be used)_

```
bme list <searched>
```

* searched is optional, only if you want to list specific commands
* Regex, match case and full word flags are supported

#### For Executing bookmark:

Basic search `bme run <searched>`

Regex search `bme run <searched> -r <my-regex*>`

##### Formatting support:

You can format command from bookmark with python formatting as such

* Use {} to be placeholder for your tuple arguments
* Use {name} to be placeholder with key name for your dictionary arguments

**Mixing tuple and dict arguments is not supported!**

Example:

Tuple:

```
bme add echo "Hello {} !"
bme run ec Jiri
```

Dictionary arguments:

```
bme add echo "Hello {name} from {location}"
bme run ec name=Jiri location=Prague
```

**or**

```
bme run ec name=\"Jiri\" location=\"Prague\"
```

##### Optional flags:

`"-e" or "--edit"` for editing command before execution

`"-r <your-regex>" or "--regex <your-regex>"` for full word search only

`"-f" or "--full-word"` for full word search only

`"-m" or "--match-case"` for search with matching case

_(Quotas can be used)_

```
bme run <your command>
```

## Sequences

Sequences are like scripts, except you don't have to search for location and manage them with different `.bashrc` or different OS specific files.
Also thanks to this, you don't have to add them to PATH.

BME will take care of storing your sequences in your `~/.bme` folder and will help you to search in them.
These sequences work from everywhere and execution is always in your current working directory.

### Commands:

**Create Sequence**

`bme seq create {name}`

Example:

`bme seq create my_sequence`

**Remove Sequence**

`bme seq rm {name}`

Example

`bme seq rm my_sequence`

**Edit Sequence**

`bme seq edit`

This will display location of json with sequences

**Add Command to Sequence**

This will add command to sequence with use of variadic arguments

    bme seq add {sequence_name} {command...}

Example:

    bme seq add my_sequence ssh jiri@192.168.1.0

**Pop Command from Sequence**

This will pop command from sequence with use of variadic arguments

    bme seq pop {sequence_name} {command...}

Example:

    bme seq pop my_sequence ssh jiri@192.168.1.0

**Sequence Run**

Runs supplied sequence, and will do search for you if not found

    bme sequence run {sequence_name}

Sequence does support formatting of dynamic arguments same way as bookmarks
these arguments will be passed to every command for formatting

Example:

    bme sequence run my_sequence John

or

    bme sequence run my_sequence name=John

**Sequence Watch (!BETA!)**

Launches sequence on file modify

    bme sequence watch {sequence_name} {file_path}

**List Sequence**

This will list commands and sequences, if argument is used search in text is applied to results

Optional flags:

    "-r <your-regex>" or "--regex <your-regex>"` for full word search only
    "-f" or "--full-word" for full word search only
    "-m" or "--match-case" for search with matching case

Example Data:

    In sequence DB there is:
     'ssh jiri@192.168.1.0' command
     'ssh jiri@192.168.1.55' command
     'scp jiri@192.168.1.55' command

Command `bme sequence list` will list all the sequences and their commands

Specific listing format:

    bme sequence list <optional commands that match this to list>

Example:

    bme sequence list ssh

Output:

```        
'ssh jiri@192.168.1.0' command
'ssh jiri@192.168.1.55' command
```

<hr>
Did I made your life less painful ? 
<br>
<br>
Support my coffee addiction ;)
<br>
<a href="https://www.buymeacoffee.com/jiriotoupal" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy me a Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
