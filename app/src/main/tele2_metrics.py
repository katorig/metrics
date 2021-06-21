#!/usr/bin/env python3

from metrics.metrics import Metrics
from metrics.metrics_catalog import *
from argparse import ArgumentParser
from utils.logs_maker import init_logger

logger = init_logger(__name__)


def define_main_args_parser(methods_list: list) -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("method",
                        nargs="?",
                        help=f"""Type name of method you want to run.
Possible methods: {', '.join(methods_list[1:])}.
Default method: no_function.
If you want to send notification add --notify parameter.""",
                        choices=methods_list,
                        default='no_function',
                        )
    parser.add_argument('--notify', metavar='notify', type=int, default=None,
                        help="type 1 for notification by email or 0 for no notification")
    return parser


if __name__ == '__main__':
    mtr = Metrics()
    methods_list = list(methods_dict.keys())
    parser = define_main_args_parser(methods_list)
    args, sub_args = parser.parse_known_args()
    methods_dict.get(args.method)(args.notify)
