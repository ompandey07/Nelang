import sys
import os
import argparse
from .interpreter import NeLangInterpreter
from . import __version__
import logging

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def setup_logger(debug=False):
    logger = logging.getLogger('nelang')
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(f"{YELLOW}[DEBUG]{RESET} %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if debug else logging.WARNING)
    return logger

def print_help():
    help_text = f"""{BOLD}{CYAN}NeLang CLI v{__version__}{RESET}

Usage:
  {BOLD}nelang{RESET} <command> [arguments]

Commands:
  {BOLD}run{RESET} <file.nl> [--debug]   Execute a NeLang script
  {BOLD}version{RESET}                   Show the version of NeLang
  {BOLD}help{RESET}                      Show this help message
"""
    print(help_text)

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1]

    if command in ("help", "--help", "-h"):
        print_help()
        sys.exit(0)
    elif command in ("version", "--version", "-v"):
        print(f"NeLang v{__version__}")
        sys.exit(0)
    elif command == "run":
        parser = argparse.ArgumentParser(prog="nelang run")
        parser.add_argument("file", help="The .nl file to execute")
        parser.add_argument("--debug", action="store_true", help="Enable debug mode and AST logging")
        args = parser.parse_args(sys.argv[2:])
            
        filepath = args.file
        if not filepath.endswith('.nl'):
            print(f"{RED}Error: File must have a .nl extension.{RESET}", file=sys.stderr)
            sys.exit(1)

        if not os.path.exists(filepath):
            print(f"{RED}Error: File '{filepath}' not found.{RESET}", file=sys.stderr)
            sys.exit(1)

        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()

        logger = setup_logger(args.debug)
        interpreter = NeLangInterpreter(logger=logger, debug=args.debug)
        interpreter.execute(source, filename=filepath)
    else:
        print(f"{RED}Error: Unknown command '{command}'{RESET}", file=sys.stderr)
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
