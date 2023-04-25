import re
import json

class Command:
    def __init__(self, app):
        self._app = app

    def execute(self, args):
        raise NotImplementedError

def from_json(command):
    command_name = None
    command_args = {}
    cmd_match: re.Match = re.search(r'^([a-z_]+) (\{.*\})$', command, re.IGNORECASE)
    if cmd_match is not None:
        command_name = cmd_match.group(1)
        command_args = json.loads(cmd_match.group(2))
    return command_name, command_args

def to_json(cmd_name: str, cmd_args: dict):
    data = "{name} {args}".format(name=cmd_name, args=json.dumps(cmd_args))
    return data
