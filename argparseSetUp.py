from argparse import  ArgumentParser

#This module exists in case developer will choose to use optparser 
#instead of argparse

def parse_arguments():
    parser = ArgumentParser(description="Folder Synchronization")
    parser.add_argument("-s", "-source", type=str, help="Source directory path")
    parser.add_argument("-r", "-replica", type=str, help="Destination directory path")
    parser.add_argument("-i", "-interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("-l", "-log", type=str, help="Log file path")
    return parser.parse_args()
