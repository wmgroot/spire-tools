import os
import sys
import importlib
import pkg_resources
import json
import argparse
from ruamel.yaml import YAML
import random
import textwrap
from datetime import datetime

from .logger import Logger

class BC:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class SPIRE():
    def __init__(self, args=None, init=True):
        if not init:
            return

        self.datetime = datetime
        self.version = pkg_resources.get_distribution('spire-tools').version

        if args == None:
            self.args = vars(self.load_arguments())
        else:
            self.args = args

        self.colors = {
            'purple': BC.PURPLE,
            'blue': BC.BLUE,
            'green': BC.GREEN,
            'yellow': BC.YELLOW,
            'red': BC.RED,
            'reset': BC.RESET,
            'bold': BC.BOLD,
            'underline': BC.UNDERLINE,
        }

        self.color_order = [
            BC.RESET,
            BC.PURPLE,
            BC.BLUE,
            BC.GREEN,
            BC.YELLOW,
            BC.RED,
        ]

        self.resistance_color_map = {
            'shadow': BC.PURPLE,
            'mind': BC.BLUE,
            'reputation': BC.GREEN,
            'silver': BC.YELLOW,
            'blood': BC.RED,

            'occult': BC.PURPLE,
            'liberty': BC.YELLOW,
            'demonic': BC.RED,
        }
        self.level_color_map = {
            'minor': BC.GREEN,
            'moderate': BC.YELLOW,
            'severe': BC.RED,
        }

        logger_params = {
            'level': self.args['log_level']
        }
        if os.getenv('DEBUG'):
            logger_params['level'] = 'debug'
        self.logger = Logger(**logger_params)

        if 'version' in self.args and self.args['version']:
            self.logger.log(self.version)
            sys.exit(0)

        self.logger.log('spire-tools version: %s' % self.version, level='debug')
        self.logger.log('args: %s' % json.dumps(self.args, indent=2, default=str), level='debug')

        yaml = YAML(typ='safe')
        self.config = yaml.load(open(self.args['tables']))

        if 'seed' not in self.args or self.args['seed'] == '':
            self.args['seed'] = self.random_alphanumeric()

        self.random = random.Random(self.args['seed'])
        self.logger.log('seed: %s' % self.args['seed'], level='debug')

    def random_alphanumeric(self, n=16):
        return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for x in range(n))

    def load_arguments(self):
        parser = argparse.ArgumentParser(description='spire options')
        self.parser = parser

        parser.add_argument('command', metavar='<command>', choices=['fallout'])

        # meta command line arguments
        parser.add_argument('-v', '--version', action='store_true', help='display the package version')
        parser.add_argument('-L', '--log_level', default='info', choices=['info', 'debug', 'warn', 'error'], help='set the desired logging level')

        # meta game data arguments
        parser.add_argument('-T', '--tables', default='%s/tables.yaml' % os.path.dirname(os.path.realpath(globals()['__file__'])), help='path to the tables file')
        parser.add_argument('-R', '--rolls_on', default=False, action='store_true', help='show rolled values')
        parser.add_argument('-S', '--seed', default='', help='sets the random generator seed')

        # game arguments
        parser.add_argument('-r', '--resistance', choices=[
            'blood',
            'mind',
            'silver',
            'shadow',
            'reputation',
            'bond',
            'liberty',
            'demonic',
            'occult',
        ], required=True, help='the name of the resistance to roll for')
        parser.add_argument('-c', '--class', default='', type=str, help='the name of the class to roll for to allow class specific fallouts')
        parser.add_argument('-l', '--level', choices=['minor', 'moderate', 'severe'], required=True, help='the severity of the fallout')
        parser.add_argument('-o', '--outcomes', default=3, type=int, help='the maximum number of results to print')

        return parser.parse_args()

    def command_fallout(self, args):
        fallout = self.filter_fallout(self.config['fallout'], args)
        fallout = self.choose_fallout(fallout, args['outcomes'])
        self.print_fallout(fallout, args)

    def filter_fallout(self, fallout, args):
        filtered = {}

        for name, f in fallout.items():
            if args['level'] != f['level']:
                self.logger.log('%s - level mismatch: %s vs %s' % (name, args['level'], f['level']), level='debug')
                continue

            if args['resistance'] not in f['resistance']:
                self.logger.log('%s - resistance mismatch: %s vs %s' % (name, args['resistance'], f['resistance']), level='debug')
                continue

            if len(args['class']) > 0 and 'class' in f:
                if args['class'] != f['class']:
                    self.logger.log('%s - class mismatch: %s vs %s' % (name, args['class'], f['class']), level='debug')
                    continue

            # add the fallout to the list of possibilities
            self.logger.log('%s - added' % name, level='debug')
            filtered[name] = f

        self.logger.log('fallout options: %s' % json.dumps(filtered, indent=2, default=str), level='debug')
        return filtered

    def choose_fallout(self, fallout, count):
        keys = list(fallout.keys())
        random.shuffle(keys)

        random_fallout = {}
        for n in range(count):
            if len(keys) <= 0:
                break
            choice = keys.pop()
            random_fallout[choice] = fallout[choice]

        return random_fallout

    def print_fallout(self, fallout, args, linked=False):
        self.logger.log()
        for name, f in fallout.items():

            title = self.color(name.replace('-', ' ').title(), self.resistance_color_map.get(args['resistance'], BC.RESET))
            level = self.color(f['level'].title(), self.level_color_map[f['level']])

            tags = []
            for r in f['resistance']:
                tags.append(self.color(r.title(), self.resistance_color_map.get(r, BC.RESET)))

            if 'class' in f:
                tags.append(f['class'].replace('-', ' ').title())

            headline = '%s (%s) - %s' % (title, level, ' / '.join(tags))
            if 'source' in f:
                headline = f"{headline} - {f['source']}"
            if linked:
                headline = f"(linked) {headline}"

            self.logger.log(headline)
            self.logger.log()
            self.logger.log(f['description'])

            if 'links' in f:
                for l in f['links']:
                    linked_fallout = {}
                    linked_fallout[l] = self.config['fallout'][l]
                    self.print_fallout(linked_fallout, args, linked=True)

    def color(self, text, color):
        if color in self.colors:
            color = self.colors[color]

        return '%s%s%s' % (color, text, BC.RESET)

    def run(self):
        getattr(self, "command_%s" % self.args['command'])(self.args)

def main():
    SPIRE().run()

if __name__ == '__main__':
    main()
