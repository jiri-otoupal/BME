# BME

(Bookmark my Executions/Commands)

Never use notepads or history for searching for your past commands. With BME you can bookmark your commands, search in your bookmarked commands and
execute them with edit possibility before execution.

[![image](https://img.shields.io/pypi/v/bme.svg)](https://pypi.org/project/bme/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bme)](https://pypi.org/project/bme/)
[![Downloads](https://pepy.tech/badge/bme)](https://pepy.tech/project/bme)
[![Upload Python Package](https://github.com/jiri-otoupal/BME/actions/workflows/python-publish.yml/badge.svg)](https://github.com/jiri-otoupal/BME/actions/workflows/python-publish.yml)

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

## All your commands are saved in ''

## Usage:

#### For adding bookmark:

_(Quotas can be used)_

```bash

bme add <your command>

```

#### For Removing bookmark:

_(Quotas can be used)_

```bash

bme rm <your command>

```

#### For List bookmarks:

_(Quotas can be used)_

```bash

bme list <searched>

```

* searched is optional, only if you want to list specific commands
* Regex, match case and full word flags are supported

#### For Executing bookmark:

Basic search `bme run <searched>`

Regex search `bme run <searched> -r <my-regex*>`

##### Optional flags:

`"-e" or "--edit"` for editing command before execution

`"-r <your-regex>" or "--regex <your-regex>"` for full word search only

`"-f" or "--full-word"` for full word search only

`"-m" or "--match-case"` for search with matching case

_(Quotas can be used)_

```bash

bme run <your command>

```

<hr>
Did I made your life less painful ? 
<br>
<br>
Support my coffee addiction ;)
<br>
<a href="https://www.buymeacoffee.com/jiriotoupal" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy me a Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
