import time
from argparseSetUp import parse_arguments
from syncApp import *

def main():
    #retrieve console output as a set of inctructions
    args = parse_arguments()
    setup_logging(args.l)

    while True:
        actions = compare_folders(args.s, args.r)
        synchronize_folders(actions)
        time.sleep(args.i)

if __name__ == "__main__":
    main()
