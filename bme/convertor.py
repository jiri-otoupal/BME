import collections


def get_cmd_str(cmd: list):
    if type(cmd) is not str:
        return ' '.join(cmd)
    else:
        return cmd
