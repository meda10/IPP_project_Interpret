import getopt, sys


def help_message():
    print("Help Message\n")
    exit(0)

def parse_options():
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['help', 'source='])
    except getopt.GetoptError as err:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)
    # output = None
    # verbose = False
    for o, a in opts:
        if o in ( "--help" ):
            help_message()
        elif o in ("--source="):
            print('%{}'.format(o))
            print('%{}'.format(a))
            # output = a
        else:
            assert False, "unhandled option"
    # ...


def main():
    parse_options()


if __name__ == "__main__":
    main()
