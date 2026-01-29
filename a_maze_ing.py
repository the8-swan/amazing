import sys
import config_validation

""""
Your program must handle all errors gracefully: invalid configuration,
file not found, bad syntax, impossible maze parameters, etc.
It must never crash unexpectedly, and must always provide a clear
error message to the user.
"""


def main():
    args = sys.argv[1:]
    if args.__len__() > 1:
        print("Too many files , make sure to enter one file !!")
    elif args.__len__() < 1:
        print("You forgot to mention the config file !!")
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                content = file.read()
                data = config_validation.config_validation(content)
                print(type(data))
        except FileNotFoundError as e:
            print(e)


if __name__ == "__main__":
    main()
