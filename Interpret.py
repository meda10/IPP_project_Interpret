import getopt
import sys
import xml.etree.ElementTree as ET


class State(object):

    # def __init__(self):

    def local_frame(self):
        ...

    def frame(self, frame: str):
        ...

    def create_frame(self):
        ...

    def push_frame(self):
        ...

    def pop_frame(self):
        ...

    def get_value(self):
        ...

    def set_value(self, to, what):
        ...

    def define_variable(self, variable):
        ...

    def call(self, op):
        ...

    def return_(self):
        ...

    def jump(self, op):
        ...

    def push_stack(self, op):
        ...

    def pop_stack(self, op=None):
        ...

    def jump_if(self, op0, op1, op2, positive=True):
        ...

    def set_char(self, where, index, from_):
        ...

    def get_char(self, target, string, index):
        ...

    def str_len(self, target, string):
        ...

    def read(self, to, type_):
        ...

    def write(self, op):
        ...

    def string_to_int_stack(self):
        ...


class Frames:

    def __init__(self):
        self.stack = []
        self.global_frame = {}

    def empty_stack(self):
        return self.stack == []

    def push(self, frame):
        self.stack.insert(0, frame)

    def pop(self):
        if not self.empty_stack():
            return self.stack.pop(0)
        else:
            return  # todo

    def top(self):
        if not self.empty_stack():
            return self.stack[0]
        else:
            return  # todo

    def get_global_frame(self):
        return self.global_frame

    def append_global_frame(self, key, value):
        self.global_frame[key] = value

    @staticmethod
    def create_frame():
        local_frame = {}
        return local_frame

    @staticmethod
    def append_frame(frame, key, value):
        frame[key] = value


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
        if o in ("--help"):
            help_message()
        elif o in ("--source="):
            print('%{}'.format(o))
            print('%{}'.format(a))
            # output = a
        else:
            assert False, "unhandled option"
    # ...


def parse_xml():
    tree = ET.parse('input.xml')
    root = tree.getroot()
    arr = []
    for child in root:
        sub_arr = []
        i = 1
        sub_arr.append(child.attrib['opcode'])
        for j in range(0, 5):
            try:
                sub_arr.append(child.find('arg{}'.format(i)).attrib['type'])
                sub_arr.append(child.find('arg{}'.format(i)).text)
                i = i + 1
            except AttributeError:
                break
        arr.append(sub_arr)
    return arr


def main():
    # arr = parse_xml()
    # print(arr)

    frame = Frames()
    d = Frames.create_frame()
    Frames.append_frame(d, 'LOL', 5)
    Frames.append_frame(d, 'FF', 'adawdwa')
    Frames.append_frame(d, 'RR', "azzzzzzzzzzzz")
    print(d)
    Frames.push(frame, d)

    d = Frames.create_frame()
    Frames.append_frame(d, 'wow', 56656)
    Frames.append_frame(d, 'NOPE', 'MMM')
    print(d)
    Frames.push(frame, d)

    d = Frames.create_frame()
    print(d)
    Frames.push(frame, d)

    print(Frames.pop(frame))
    print(Frames.pop(frame))
    print(Frames.pop(frame))
    print(Frames.pop(frame))
    print(Frames.pop(frame))
    print(Frames.top(frame))

    print(Frames.get_global_frame(frame))

    Frames.append_global_frame(frame, 'hell', 585)
    print(Frames.get_global_frame(frame))


if __name__ == "__main__":
    main()
