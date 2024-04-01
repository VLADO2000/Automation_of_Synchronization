import time
from argparseSetUp import parse_arguments
from syncApp import setup_logging, compare_folders, synchronize_folders


def main():
    #retrieve console output as a set of inctructions
    args = parse_arguments()
    setup_logging(args.l)
    while True:
        actions = compare_folders(args.s, args.r)
        synchronize_folders(actions)
        print(f"Folder synchronization interval is set to {args.i} seconds. If you want to stop " \
                "press Ctrl+C - otherwise the app will restart automatically")         
        time.sleep(args.i)

if __name__ == "__main__":
    main()
