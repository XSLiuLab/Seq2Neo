import sys
from seq2neo.lib.arg_main import MainArgumentParser


def define_argparse():
    return MainArgumentParser().parser


def main():
    parser = define_argparse()
    args = parser.parse_known_args()
    try:
        args[0].func.main(args[1])
    except AttributeError as e:
        parser.print_help()
        print("Error: No command specified")
        sys.exit(-1)


if __name__ == "__main__":
    main()
