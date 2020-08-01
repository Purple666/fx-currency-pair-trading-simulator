import argparse
from .date_validator import valid_date
from .config_file.parse_general_args import SUPPORTED_CURRENCY_PAIRS
from .config_file.signal_strat.parse_signal_strat_args import MA_FUNCTIONS


def create_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Trading simulator for FX currency-pairs')
    cmd_subparsers = parser.add_subparsers(dest='command', required=True)

    init_parser = cmd_subparsers.add_parser('init')
    add_simulation_config_argument(init_parser)

    run_parser = cmd_subparsers.add_parser('run')
    add_simulation_config_argument(run_parser)
    run_parser.add_argument('--id', type=str, help='identifier for the simulation')
    run_parser.add_argument('--plot_timeseries','--plot_ts', action='store_true', help='generate time series plot of simulation')

    clean_parser = cmd_subparsers.add_parser('clean')
    clean_parser.add_argument('--id', type=str, help='identifier for the simulation')
    return parser


def add_simulation_config_argument(parser):
    config_subparsers = parser.add_subparsers(dest='config', required=True)
    config_file_parser = config_subparsers.add_parser('file')
    config_file_parser.add_argument('config_file', type=str, help='path to configuration file')
    config_args_parser = config_subparsers.add_parser('args')
    add_simulation_arguments(config_args_parser)


def add_simulation_arguments(parser):
    parser.add_argument('currency_pair', type=str, help='name of FX currency-pair', choices=SUPPORTED_CURRENCY_PAIRS)
    parser.add_argument('--start', type=valid_date, help='UTC starting date for the simulation (earliest if not specified)')
    parser.add_argument('--stop', type=valid_date, help='UTC stopping date for the simulation (latest if not specified)')
    parser.add_argument('--ma', type=str, help='moving average function', choices=MA_FUNCTIONS, required=True)
    parser.add_argument('--short', type=int, help='window for short moving average (in minutes)', required=True)
    parser.add_argument('--long', type=int, help='window for moving long average (in minutes)', required=True)
    parser.add_argument('--quote', type=str, help='the bid quote to use', choices=['open', 'close', 'high', 'low'], required=True)
    parser.add_argument('--delta', type=int, help='magnitude in pips short average must differ from long average to be considred a break', required=True)
    parser.add_argument('--no-cache', '--nc', action='store_true', help='ignore caches and load data from source')
    parser.add_argument('--reverse', '--r', action='store_true', help='close positions when a reversed signal is encountered')

    stop_strat_subparsers = parser.add_subparsers(dest='stopping_strat', help='strategy for evaluating stopping criteria',  required=True)
    offset_strat_parser = stop_strat_subparsers.add_parser('offset')
    offset_strat_parser.add_argument('--profit', type=int, help='delta pips for setting stop profit', required=True)
    offset_strat_parser.add_argument('--loss', type=int, help='delta pips for setting stop loss', required=True)
    fib_strat_parser = stop_strat_subparsers.add_parser('fib')
    fib_strat_parser.add_argument('--lookback', '--lb', type=int, help='duration (in minutes) to look back when evaluating stopping criteria', required=True)