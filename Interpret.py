import getopt
import sys
import xml.etree.ElementTree as Et
import re

instructions = ["MOVE", "CREATEFRAME", "PUSHFRAME", "POPFRAME", "DEFVAR", "CALL", "RETURN", "PUSHS",
                "POPS", "ADD", "SUB", "MUL", "IDIV", "LT", "GT", "EQ", "AND", "OR", "NOT", "INT2CHAR",
                "STRI2INT", "READ", "WRITE", "CONCAT", "STRLEN", "GETCHAR", "SETCHAR", "TYPE",
                "JUMP", "JUMPIFEQ", "JUMPIFNEQ", "DPRINT", "BREAK"] # , "LABEL"


class State(object):

    def __init__(self, array):
        self.array = array
        self.current_ins = []
        self.data_stack = Frames()
        self.frame = Frames()
        self.function_dic = {
            "MOVE": self.move,
            "CREATEFRAME": self.create_frame,
            "PUSHFRAME": self.push_frame,
            "POPFRAME": self.pop_frame,
            "DEFVAR": self.def_var,
            "CALL": self.call,
            "RETURN": self.return_,
            "PUSHS": self.push_stack,
            "POPS": self.pop_stack,
            "ADD": self.add,
            "SUB": self.sub,
            "MUL": self.mul,
            "IDIV": self.idiv,
            "LT": self.lt,
            "GT": self.gt,
            "EQ": self.eq,
            "AND": self.and_,
            "OR": self.or_,
            "NOT": self.not_,
            "INT2CHAR": self.int_to_char,
            "STRI2INT": self.string_to_int,
            "READ": self.read,
            "WRITE": self.write,
            "CONCAT": self.concat,
            "STRLEN": self.str_len,
            "GETCHAR": self.get_char,
            "SETCHAR": self.set_char,
            "TYPE": self.type,
            "LABEL": self.label,
            "JUMP": self.jump,
            "JUMPIFEQ": self.jump_if_eq,
            "JUMPIFNEQ": self.jump_if_neq,
            "DPRINT": self.dprint,
            "BREAK": self.break_,
        }
        self.temp_frame = None
        self.ins_counter = 0

    def interpret(self):

        while 1:
            try:
                self.current_ins = self.array[self.ins_counter]
                self.ins_counter += 1
                if self.current_ins[1] == "LABEL":
                    self.function_dic[self.current_ins[1]]()
            except IndexError:
                break

        self.ins_counter = 0

        while 1:
            try:
                self.current_ins = self.array[self.ins_counter]
                self.ins_counter += 1
                for j in instructions:
                    if self.current_ins[1] == j:
                        # print(j)
                        self.function_dic[self.current_ins[1]]()
            except IndexError:
                break
                #exit(1562) #todo wtf error

            # print(self.current_ins)

        """
        for self.current_ins in self.array:
            for j in instructions:
                if self.current_ins[1] == j:
                    print(j)
                    self.function_dic[self.current_ins[1]]()
            # print(self.current_ins)
        """

    def move(self):
        if len(self.current_ins) == 6:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
        else:
            exit(52)

        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        value = self.var_value(self.current_ins[4], self.current_ins[5])
        self.var_write(frame, key, value)

    def create_frame(self):
        if not len(self.current_ins) == 2:
            exit(52)
        self.temp_frame = Frames.create_frame()

    def push_frame(self):
        if not len(self.current_ins) == 2:
            exit(52)
        if self.temp_frame is not None:
            self.frame.push(self.temp_frame)
            self.temp_frame = None
        else:
            exit(55)

    def pop_frame(self):
        if not len(self.current_ins) == 2:
            exit(52)
        if self.frame.get_local_frame() is not None:
            self.temp_frame = self.frame.pop()
        else:
            exit(55)

    def def_var(self):
        if len(self.current_ins) == 4:
            Check.variable_check(self.current_ins[3])
        else:
            exit(52)

        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]

        if frame == "GF":
            self.frame.append_global_frame(key, None)
        elif frame == "LF":
            self.frame.append_local_frame(key, None)
        elif frame == "TF":
            if self.temp_frame is not None:
                Frames.append_frame(self.temp_frame, key, None)
            else:
                exit(55)

    def call(self):
        if len(self.current_ins) == 3:
            Check.label_check(self.current_ins[2])
        else:
            exit(52)

        print(self.current_ins)
        print("Call")
        ...

    def return_(self):
        if not len(self.current_ins) == 1:
            exit(52)

        print(self.current_ins)
        print("Return")
        ...

    def push_stack(self):
        if len(self.current_ins) == 4:
            Check.symbol_check(self.current_ins[3])
        else:
            exit(52)

        symbol = self.current_ins[3]
        self.data_stack.push(symbol)

    def pop_stack(self):
        if len(self.current_ins) == 4:
            Check.variable_check(self.current_ins[3])
        else:
            exit(52)

        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        value = self.data_stack.pop()
        self.var_write(frame, key, value)

    def add(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(52)

        try:
            val_1 = int(self.var_value(self.current_ins[4], self.current_ins[5]))
            val_2 = int(self.var_value(self.current_ins[6], self.current_ins[7]))
        except ValueError:
            exit(53)
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        value = val_1 + val_2
        self.var_write(frame, key, value)

    def sub(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(52)

        try:
            val_1 = int(self.var_value(self.current_ins[4], self.current_ins[5]))
            val_2 = int(self.var_value(self.current_ins[6], self.current_ins[7]))
        except ValueError:
            exit(53)
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        value = val_1 - val_2
        self.var_write(frame, key, value)

    def mul(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(52)

        try:
            val_1 = int(self.var_value(self.current_ins[4], self.current_ins[5]))
            val_2 = int(self.var_value(self.current_ins[6], self.current_ins[7]))
        except ValueError:
            exit(53)
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        value = val_1 * val_2
        self.var_write(frame, key, value)

    def idiv(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(52)

        try:
            val_1 = int(self.var_value(self.current_ins[4], self.current_ins[5]))
            val_2 = int(self.var_value(self.current_ins[6], self.current_ins[7]))
        except ValueError:
            exit(53)
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        try:
            value = val_1 // val_2
        except ZeroDivisionError:
            exit(57)
        self.var_write(frame, key, value)

    def lt(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(52)

        val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
        val_2 = self.var_value(self.current_ins[6], self.current_ins[7])
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        if val_1 < val_2:
            self.var_write(frame, key, "true")
        else:
            self.var_write(frame, key, "false")

    def gt(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(52)

        val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
        val_2 = self.var_value(self.current_ins[6], self.current_ins[7])
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        if val_1 > val_2:
            self.var_write(frame, key, "true")
        else:
            self.var_write(frame, key, "false")

    def eq(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(52)

        val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
        val_2 = self.var_value(self.current_ins[6], self.current_ins[7])
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        if val_1 == val_2:
            self.var_write(frame, key, "true")
        else:
            self.var_write(frame, key, "false")

    def and_(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(52)

        val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
        val_2 = self.var_value(self.current_ins[6], self.current_ins[7])
        Check.bool_check(val_1)
        Check.bool_check(val_2)
        if val_1 == "false":
            val_1 = False
        if val_2 == "false":
            val_2 = False
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        if bool(val_1) and bool(val_2):
            self.var_write(frame, key, "true")
        else:
            self.var_write(frame, key, "false")

    def or_(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(52)

        val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
        val_2 = self.var_value(self.current_ins[6], self.current_ins[7])
        Check.bool_check(val_1)
        Check.bool_check(val_2)
        if val_1 == "false":
            val_1 = False
        if val_2 == "false":
            val_2 = False
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        if bool(val_1) or bool(val_2):
            self.var_write(frame, key, "true")
        else:
            self.var_write(frame, key, "false")

    def not_(self):
        if len(self.current_ins) == 6:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
        else:
            exit(52)

        val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
        Check.bool_check(val_1)
        if val_1 == "false":
            val_1 = False
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        if not bool(val_1):
            self.var_write(frame, key, "true")
        else:
            self.var_write(frame, key, "false")

    def int_to_char(self):
        if len(self.current_ins) == 6:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
        else:
            exit(52)

        try:
            val_1 = int(self.var_value(self.current_ins[4], self.current_ins[5]))
        except ValueError:
            exit(53)
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        try:
            value = chr(val_1)
        except ValueError:
            exit(58)
        self.var_write(frame, key, value)

    def string_to_int(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(52)

        try:
            val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
            val_2 = int(self.var_value(self.current_ins[6], self.current_ins[7]))
        except ValueError:
            exit(53)
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        try:
            value = ord(val_1[val_2])
        except IndexError:
            exit(58)
        self.var_write(frame, key, value)

    def read(self):
        if len(self.current_ins) == 6:
            Check.variable_check(self.current_ins[3])
            Check.type_check(self.current_ins[5])
        else:
            exit(52)

        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        type_ = self.current_ins[5]
        value = input()
        if type_ == "int":
            try:
                Check.int_check(value)
                value = int(value)
                self.var_write(frame, key, value)
            except:  # todo raise exceptions
                self.var_write(frame, key, 0)
        elif type_ == "string":
            try:
                Check.string_check(value)
                value = str(value)
                self.var_write(frame, key, value)
            except:  # todo raise exceptions
                self.var_write(frame, key, "")
        elif type_ == "bool":
            value = value.lower()
            try:
                Check.bool_check(value)
                if value == "false":
                    value = False
                value = bool(value)
                self.var_write(frame, key, value)
            except:  # todo raise exceptions
                self.var_write(frame, key, "false")

    def write(self):
        if len(self.current_ins) == 4:
            Check.symbol_check(self.current_ins[3])
        else:
            exit(52)

        val = self.var_value(self.current_ins[2], self.current_ins[3])
        val.encode('utf-8').decode('utf-8')
        print(val)  # todo bool \024 sequence

    def concat(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(52)

        val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
        val_2 = self.var_value(self.current_ins[6], self.current_ins[7])
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        value = val_1 + val_2
        self.var_write(frame, key, value)

    def str_len(self):
        if len(self.current_ins) == 6:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
        else:
            exit(52)

        val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        value = len(val_1)
        self.var_write(frame, key, value)

    def get_char(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(52)

        try:
            val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
            val_2 = int(self.var_value(self.current_ins[6], self.current_ins[7]))
        except ValueError:
            exit(53)
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        try:
            value = val_1[val_2]
        except IndexError:
            exit(58)
        self.var_write(frame, key, value)

    def set_char(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(52)

        try:
            val_1 = self.var_value(self.current_ins[2], self.current_ins[3])
            val_2 = int(self.var_value(self.current_ins[4], self.current_ins[5]))
            val_3 = self.var_value(self.current_ins[6], self.current_ins[7])[0]
        except ValueError:
            exit(53)
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        try:
            val_1 = val_1[:val_2] + val_3 + val_1[val_2+1:]
            v = val_2 + 1
            if v > len(val_1): # todo 1
                raise IndexError
        except IndexError:
            exit(58)
        self.var_write(frame, key, val_1)

    def type(self): # todo typpe
        if len(self.current_ins) == 6:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
        else:
            exit(52)

        val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        try:
            Check.string_check(val_1)
            self.var_write(frame, key, "string")
        except:
            pass

        try:
            Check.int_check(val_1)
            self.var_write(frame, key, "int")
        except:
            pass

        try:
            Check.bool_check(val_1)
            self.var_write(frame, key, "bool")
        except:
            pass

    def label(self):
        if len(self.current_ins) == 4:
            Check.label_check(self.current_ins[2])
        else:
            exit(52)

        label = self.current_ins[3]
        instruction_number = self.current_ins[0]
        if label not in self.frame.get_label():
            self.frame.append_label(label, instruction_number)
        else:
            exit(52)

    def jump(self):
        if len(self.current_ins) == 4:
            Check.label_check(self.current_ins[3])
        else:
            exit(52)

        key = self.current_ins[3]

        if key in self.frame.get_label():
            self.ins_counter = int(self.frame.get_label()[key])
        else:
            exit(52)

    def jump_if_eq(self):
        if len(self.current_ins) == 8:
            Check.label_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(52)

        key = self.current_ins[3]

        val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
        val_2 = self.var_value(self.current_ins[6], self.current_ins[7])

        if val_1 == val_2:
            if key in self.frame.get_label():
                self.ins_counter = int(self.frame.get_label()[key])
            else:
                exit(52)

    def jump_if_neq(self):
        if len(self.current_ins) == 8:
            Check.label_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(52)

        key = self.current_ins[3]

        val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
        val_2 = self.var_value(self.current_ins[6], self.current_ins[7])

        if val_1 != val_2:
            if key in self.frame.get_label():
                self.ins_counter = int(self.frame.get_label()[key])
                print("JUMPING")
            else:
                exit(52)
        else:
            print("NOT JUMPING")

    def dprint(self):
        if len(self.current_ins) == 4:
            Check.symbol_check(self.current_ins[3])
        else:
            exit(52)

        val = self.var_value(self.current_ins[2], self.current_ins[3])
        # val.encode('utf-8').decode('utf-8')
        print("{}".format(val), file = sys.stderr) # todo bool \024 sequence

    def break_(self):
        if not len(self.current_ins) == 2:
            exit(52)

        print("Stav Interpretu:\n"
              "Počet vykonaných instrukcí: {}\n"
              "Globální rámec: {}\n"
              "Local Frame: {}\n"
              "Temp Frame: {}\n"
              .format(self.ins_counter, self.frame.get_global_frame(), self.frame.get_local_frame(),
                      self.temp_frame), file = sys.stderr)

    def var_value(self, value_1, value_2):
        if value_1 == "var":
            frame = value_2[:2]
            key = value_2[3:]
            if frame == "GF":
                if key in self.frame.get_global_frame():
                    val = self.frame.get_global_frame()[key]
                    return val
                else:
                    exit(100)  # todo exit
            elif frame == "LF":
                if key in self.frame.get_local_frame():
                    val = self.frame.get_local_frame()[key]
                    return val
                else:
                    exit(100)  # todo exit
            elif frame == "TF":
                if self.temp_frame is not None:
                    if key in self.temp_frame:
                        val = self.temp_frame[key]
                        return val
                    else:
                        exit(100)  # todo exit
                else:
                    exit(55)
        else:
            val = value_2
            return val

    def var_write(self, frame, key, value):
        if value is None:
            value = ""

        if frame == "GF":
            if key in self.frame.get_global_frame():
                self.frame.append_global_frame(key, value)
            else:
                exit(100)  # todo exit
        elif frame == "LF":
            if key in self.frame.get_local_frame():
                self.frame.append_local_frame(key, value)
            else:
                exit(100)  # todo exit
        elif frame == "TF":
            if self.temp_frame is not None:
                if key in self.temp_frame:
                    Frames.append_frame(self.temp_frame, key, value)
                else:
                    exit(100)  # todo exit
            else:
                exit(55)


class Frames:

    def __init__(self):
        self.stack = []
        self.global_frame = {}
        self.label = {}

    def empty_stack(self):
        return self.stack == []

    def push(self, frame):
        self.stack.insert(0, frame)

    def pop(self):
        if not self.empty_stack():
            return self.stack.pop(0)
        else:
            exit(55)

    def get_local_frame(self):
        if not self.empty_stack():
            return self.stack[0]
        else:
            exit(55)

    def get_label(self):
        return self.label

    def get_global_frame(self):
        return self.global_frame

    def append_global_frame(self, key, value):
        self.global_frame[key] = value

    def append_label(self, key, value):
        self.label[key] = value

    def append_local_frame(self, key, value):
        if not self.empty_stack():
            Frames.append_frame(self.stack[0], key, value)
        else:
            exit(55)

    @staticmethod
    def create_frame():
        frame = {}
        return frame

    @staticmethod
    def append_frame(frame, key, value):
        frame[key] = value


class Check(object):

    # def __init__(self, li):
    # self.li = li
    # ...

    @staticmethod
    def variable_check(text):
        regex = r"^(LF|GF|TF)\@(\w|\_|\-|\$|\&|\%|\*)(?<=\D)(\w|\_|\-|\$|\&|\%|\*)*$"
        matches = re.search(regex, text, re.UNICODE)
        if matches:
            return True
        else:
            exit(52)

    @staticmethod
    def symbol_check(text):
        if Check.string_check(text):
            return True
        elif Check.bool_check(text):
            return True
        elif Check.int_check(text):
            return True
        elif Check.variable_check(text):
            return True
        else:
            exit(52)

    @staticmethod
    def string_check(text):
        if text is None:
            return True
        regex = r"^((\\\d{3})|([^\\#\s]))*$"
        matches = re.search(regex, text, re.UNICODE)
        if matches:
            return True
        else:
            exit(52)

    @staticmethod
    def int_check(text):
        regex = r"^[-+]?\d+$"
        matches = re.search(regex, text, re.UNICODE)
        if matches:
            return True
        else:
            exit(52)

    @staticmethod
    def bool_check(text):
        regex = r"^(true|false)$"
        matches = re.search(regex, text, re.UNICODE)
        if matches:
            return True
        else:
            exit(52)

    @staticmethod
    def label_check(text):
        regex = r"^(\w|\_|\-|\$|\&|\%|\*)(?<=\D)(\w|\_|\-|\$|\&|\%|\*)*$"
        matches = re.search(regex, text, re.UNICODE)
        if matches:
            return True
        else:
            exit(52)

    @staticmethod
    def type_check(text):
        regex = r"^(int|bool|string)$"
        matches = re.search(regex, text, re.UNICODE)
        if matches:
            return True
        else:
            exit(52)


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
        if o in "--help":
            help_message()
        elif o in "--source=":
            print('%{}'.format(o))
            print('%{}'.format(a))
            # output = a
        else:
            assert False, "unhandled option"
    # ...


def parse_xml():
    tree = Et.parse('input.xml')
    root = tree.getroot()
    arr = []
    for child in root:
        sub_arr = []
        i = 1
        sub_arr.append(child.attrib['order']) #todo
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
    arr = parse_xml()
    print(arr)
    s = State(arr)
    State.interpret(s)

    """
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

    print(Check.string_check())
    """


if __name__ == "__main__":
    main()
