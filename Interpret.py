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
        self.return_to = Frames()
        self.test = None
        self.file = open("out", "w")

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
        # print(self.frame.get_label())

        while 1:
            try:
                self.current_ins = self.array[self.ins_counter]
                self.ins_counter += 1
                for j in instructions:
                    if self.current_ins[1] == j:
                        # print("{} {}".format(self.ins_counter, j))
                        self.function_dic[self.current_ins[1]]()
            except IndexError:
                break
                #exit(1562) #todo wtf error

        self.file.close()

    def move(self):
        if len(self.current_ins) == 6:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
        else:
            exit(32)

        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        value = self.var_value(self.current_ins[4], self.current_ins[5])
        self.var_write(frame, key, value)

    def create_frame(self):
        if not len(self.current_ins) == 2:
            exit(32)
        self.temp_frame = Frames.create_frame()

    def push_frame(self):
        if not len(self.current_ins) == 2:
            exit(32)
        if self.temp_frame is not None:
            self.frame.push(self.temp_frame)
            self.temp_frame = None
        else:
            exit(55)

    def pop_frame(self):
        if not len(self.current_ins) == 2:
            exit(32)
        if self.frame.get_local_frame() is not None:
            self.temp_frame = self.frame.pop()
        else:
            exit(55)

    def def_var(self):
        if len(self.current_ins) == 4:
            Check.variable_check(self.current_ins[3])
        else:
            exit(32)

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
        if len(self.current_ins) == 4:
            Check.label_check(self.current_ins[3])
        else:
            exit(32)

        key = self.current_ins[3]
        self.return_to.push(int(self.current_ins[0]))

        if key in self.frame.get_label():
            self.ins_counter = int(self.frame.get_label()[key])
        else:
            exit(52)

    def return_(self):
        if not len(self.current_ins) == 2:
            exit(32)

        if not self.return_to.empty_stack():
            jump_to = self.return_to.pop()
            self.ins_counter = int(jump_to)
        else:
            exit(56)

    def push_stack(self):
        if len(self.current_ins) == 4:
            Check.symbol_check(self.current_ins[3])
        else:
            exit(32)

        value = self.var_value(self.current_ins[2], self.current_ins[3])
        self.data_stack.push(value)

    def pop_stack(self):
        if len(self.current_ins) == 4:
            Check.variable_check(self.current_ins[3])
        else:
            exit(32)

        frame = self.current_ins[3][:2]
        key = self.current_ins[3][3:]
        try:
            value = self.data_stack.pop()
            self.var_write(frame, key, value)
        except SystemExit:
            exit(56)

    def add(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(32)

        try:
            val_1 = int(self.var_value(self.current_ins[4], self.current_ins[5]))
            val_2 = int(self.var_value(self.current_ins[6], self.current_ins[7]))

            frame = self.current_ins[3][:2]
            key = self.current_ins[3][3:]
            value = val_1 + val_2

            self.var_write(frame, key, value)
        except ValueError:
            exit(53)

    def sub(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(32)

        try:
            val_1 = int(self.var_value(self.current_ins[4], self.current_ins[5]))
            val_2 = int(self.var_value(self.current_ins[6], self.current_ins[7]))

            frame = self.current_ins[3][:2]
            key = self.current_ins[3][3:]
            value = val_1 - val_2

            self.var_write(frame, key, value)
        except ValueError:
            exit(53)

    def mul(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(32)

        try:
            val_1 = int(self.var_value(self.current_ins[4], self.current_ins[5]))
            val_2 = int(self.var_value(self.current_ins[6], self.current_ins[7]))

            frame = self.current_ins[3][:2]
            key = self.current_ins[3][3:]
            value = val_1 * val_2

            self.var_write(frame, key, value)
        except ValueError:
            exit(53)

    def idiv(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(32)

        try:
            val_1 = int(self.var_value(self.current_ins[4], self.current_ins[5]))
            val_2 = int(self.var_value(self.current_ins[6], self.current_ins[7]))
            try:
                key = self.current_ins[3][3:]
                frame = self.current_ins[3][:2]
                value = val_1 // val_2

                self.var_write(frame, key, value)
            except ZeroDivisionError:
                exit(57)
        except ValueError:
            exit(53)

    def lt(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(32)

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
            exit(32)

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
            exit(32)

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
            exit(32)

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
            exit(32)

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
            exit(32)

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
            exit(32)

        try:
            val_1 = int(self.var_value(self.current_ins[4], self.current_ins[5]))
            frame = self.current_ins[3][:2]
            key = self.current_ins[3][3:]
            try:
                value = chr(val_1)
                self.var_write(frame, key, value)
            except ValueError:
                exit(58)
        except ValueError:
            exit(53)

    def string_to_int(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(32)

        try:
            val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
            val_2 = int(self.var_value(self.current_ins[6], self.current_ins[7]))
            val_1 = self.to_string_format(val_1)

            frame = self.current_ins[3][:2]
            key = self.current_ins[3][3:]
            try:
                value = ord(val_1[val_2])
                self.var_write(frame, key, value)
            except IndexError:
                exit(58)
        except ValueError:
            exit(53)

    def read(self):
        if len(self.current_ins) == 6:
            Check.variable_check(self.current_ins[3])
            Check.type_check(self.current_ins[5])
        else:
            exit(32)

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
            exit(32)
        # todo bool
        val = self.var_value(self.current_ins[2], self.current_ins[3])

        regex = r'\\\d{3}'
        test_str = str(val)
        match = re.search(regex, test_str)
        if match:
            string_to_print = test_str
            for a in re.findall(regex, test_str):
                sub = str("\\\\" + a[1:])
                char = str(chr(int(a[2:])))
                if char == '\\':
                    char += '\\'
                string_to_print = re.sub(sub, char, string_to_print)
            print("{}".format(string_to_print))
            self.file.write("{}".format(string_to_print))
        else:
            try:
                a = int(test_str)
                self.file.write(" {}".format(a))
                print(" {}".format(test_str))
            except ValueError:
                self.file.write("{}".format(test_str))
                print("{}".format(test_str))

    def concat(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(32)
        # todo jen retezce
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
            exit(32)

        val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
        val_1 = self.to_string_format(val_1)

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
            exit(32)

        try:
            val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
            val_2 = int(self.var_value(self.current_ins[6], self.current_ins[7]))
            val_1 = self.to_string_format(val_1)

            frame = self.current_ins[3][:2]
            key = self.current_ins[3][3:]
            try:
                value = val_1[val_2]
                self.var_write(frame, key, value)
            except IndexError:
                exit(58)
        except ValueError:
            exit(53)

    def set_char(self):
        if len(self.current_ins) == 8:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
            Check.symbol_check(self.current_ins[7])
        else:
            exit(32)

        try:
            val_1 = self.var_value(self.current_ins[2], self.current_ins[3])
            val_2 = int(self.var_value(self.current_ins[4], self.current_ins[5]))
            val_3 = self.var_value(self.current_ins[6], self.current_ins[7])[0]
            frame = self.current_ins[3][:2]
            key = self.current_ins[3][3:]
            try:
                val_1 = val_1[:val_2] + val_3 + val_1[val_2 + 1:]
                v = val_2 + 1
                if v > len(val_1):  # todo 1
                    raise IndexError
            except IndexError:
                exit(58)
            self.var_write(frame, key, val_1)
        except ValueError:
            exit(53)

    def type(self):  # todo typpe
        if len(self.current_ins) == 6:
            Check.variable_check(self.current_ins[3])
            Check.symbol_check(self.current_ins[5])
        else:
            exit(32)

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
            exit(32)

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
            exit(32)

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
            exit(32)

        key = self.current_ins[3]

        val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
        val_2 = self.var_value(self.current_ins[6], self.current_ins[7])

        try:
            val_1 = int(val_1)
            val_2 = int(val_2)
        except ValueError:
            val_1 = str(val_1)
            val_2 = str(val_2)
        finally:
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
            exit(32)

        key = self.current_ins[3]

        val_1 = self.var_value(self.current_ins[4], self.current_ins[5])
        val_2 = self.var_value(self.current_ins[6], self.current_ins[7])

        try:
            val_1 = int(val_1)
            val_2 = int(val_2)
        except ValueError:
            val_1 = str(val_1)
            val_2 = str(val_2)
        finally:
            if val_1 != val_2:
                if key in self.frame.get_label():
                    self.ins_counter = int(self.frame.get_label()[key])
                else:
                    exit(52)

        """
        if val_1 != val_2:
            if key in self.frame.get_label():
                self.ins_counter = int(self.frame.get_label()[key])
                # print("JUMPING from {} to {}\n".format(self.current_ins[0], int(self.frame.get_label()[key])))
            else:
                exit(52)
        else:
            ...
            # print("NOT JUMP {}\n".format(int(self.frame.get_label()[key])))
        """

    def dprint(self):
        if len(self.current_ins) == 4:
            Check.symbol_check(self.current_ins[3])
        else:
            exit(32)

        value = self.var_value(self.current_ins[2], self.current_ins[3])
        value = self.to_string_format(value)
        print("{}".format(value), file = sys.stderr)

        """
        regex = r'\\\d{3}'
        string = str(val)
        match = re.search(regex, string)
        if match:
            string_to_print = string
            for a in re.findall(regex, string):
                sub = str("\\\\" + a[1:])
                char = str(chr(int(a[2:])))
                if char == '\\':
                    char += '\\'
                string_to_print = re.sub(sub, char, string_to_print)
                print("{}".format(string_to_print), file = sys.stderr)
        else:
            print("{}".format(string), file = sys.stderr)
        """

    def break_(self):
        if not len(self.current_ins) == 2:
            exit(32)

        print("Stav Interpretu:\n"
              "Počet vykonaných instrukcí: {}\n"
              "Global Frame: {}"
              .format(self.current_ins[0], self.frame.get_global_frame()), file = sys.stderr)
        try:
            print("Local Frame: {}".format(self.frame.get_local_frame()), file = sys.stderr)
        except SystemExit:
            print("Local Frame: None", file = sys.stderr)

        print("Temp Frame: {}".format(self.temp_frame), file = sys.stderr)
        print("Data stack: {}\n".format(self.data_stack.get_stack()), file = sys.stderr)

    def var_value(self, value_1, value_2):
        if value_2 is None:
            return ''
        if value_1 == "var":
            frame = value_2[:2]
            key = value_2[3:]
            if frame == "GF":
                if key in self.frame.get_global_frame():
                    val = self.frame.get_global_frame()[key]
                    return val
                else:
                    exit(54)  # todo exit
            elif frame == "LF":
                if key in self.frame.get_local_frame():
                    val = self.frame.get_local_frame()[key]
                    return val
                else:
                    exit(54)  # todo exit
            elif frame == "TF":
                if self.temp_frame is not None:
                    if key in self.temp_frame:
                        val = self.temp_frame[key]
                        return val
                    else:
                        exit(54)  # todo exit
                else:
                    exit(55)
        else:
            val = value_2
            if value_1 == 'string':
                return str(val)
            if value_1 == 'int':
                return int(val)
            else:
                return val

    def var_write(self, frame, key, value):
        if value is None:
            value = ""

        if frame == "GF":
            if key in self.frame.get_global_frame():
                self.frame.append_global_frame(key, value)
            else:
                exit(54)
        elif frame == "LF":
            if key in self.frame.get_local_frame():
                self.frame.append_local_frame(key, value)
            else:
                exit(54)  # todo exit
        elif frame == "TF":
            if self.temp_frame is not None:
                if key in self.temp_frame:
                    Frames.append_frame(self.temp_frame, key, value)
                else:
                    print(key)
                    print(self.current_ins)
                    print(self.temp_frame)
                    exit(542)  # todo exit
            else:
                exit(55)

    @staticmethod
    def to_string_format(value):
        regex = r'\\\d{3}'
        test_str = str(value)
        match = re.search(regex, test_str)
        if match:
            string_to_print = test_str
            for a in re.findall(regex, test_str):
                sub = str("\\\\" + a[1:])
                char = str(chr(int(a[1:])))
                if char == '\\':
                    char += '\\'
                string_to_print = re.sub(sub, char, string_to_print)
            return string_to_print
        else:
            return test_str


class Frames:

    def __init__(self):
        self.stack = []
        self.global_frame = {}
        self.label = {}

    def empty_stack(self):
        return self.stack == []

    def get_stack(self):
        return self.stack

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

    @staticmethod
    def variable_check(text):
        regex = r"^(LF|GF|TF)\@(\w|\_|\-|\$|\&|\%|\*)(?<=\D)(\w|\_|\-|\$|\&|\%|\*)*$"
        matches = re.search(regex, text, re.UNICODE)
        if matches:
            return True
        else:
            exit(53)

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
            exit(53)

    @staticmethod
    def string_check(text):
        if text is None:
            return True
        regex = r"^((\\\d{3})|([^\\#\s]))*$"
        matches = re.search(regex, text, re.UNICODE)
        if matches:
            return True
        else:
            exit(53)

    @staticmethod
    def int_check(text):
        regex = r"^[-+]?\d+$"
        matches = re.search(regex, text, re.UNICODE)
        if matches:
            return True
        else:
            exit(53)

    @staticmethod
    def bool_check(text):
        regex = r"^(true|false)$"
        matches = re.search(regex, text, re.UNICODE)
        if matches:
            return True
        else:
            exit(53)

    @staticmethod
    def label_check(text):
        regex = r"^(\w|\_|\-|\$|\&|\%|\*)(?<=\D)(\w|\_|\-|\$|\&|\%|\*)*$"
        matches = re.search(regex, text, re.UNICODE)
        if matches:
            return True
        else:
            exit(53)

    @staticmethod
    def type_check(text):
        regex = r"^(int|bool|string)$"
        matches = re.search(regex, text, re.UNICODE)
        if matches:
            return True
        else:
            exit(53)


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
    try:
        tree = Et.parse('src.xml')
    except SyntaxError:
        exit(31)
    root = tree.getroot()
    arr = []
    expected = 1

    for child in root:
        ins_c = 0
        arg1_c = 0
        arg2_c = 0
        arg3_c = 0
        sub_arr = []
        i = 1
        if child.tag != 'instruction':
            exit(31)
        try:
            if len(child.attrib) != 2:
                exit(31)

            ins = child.attrib['order']
            # if int(ins) == expected:
            sub_arr.append(child.attrib['order'])
            sub_arr.append(child.attrib['opcode'])
            expected += 1
            # else:
                # exit(32)
        except (KeyError, ValueError):
            print("Chyba v číslování instrukcí ve vstupním XML dokumentu", file = sys.stderr)
            exit(32)

        if len(child.getchildren()) > 3:
            exit(31)

        for a in child.iter():
            if a.tag == 'instruction':
                ins_c += 1
            if a.tag == 'arg1':
                arg1_c += 1
            if a.tag == 'arg2':
                arg2_c += 1
            if a.tag == 'arg3':
                arg3_c += 1
            if a.tag != 'instruction' and a.tag != 'arg1' and a.tag != 'arg2' and a.tag != 'arg3':
                exit(31)
            for b in a.attrib.keys():
                if b != 'order' and b != 'opcode' and b != 'type':
                    exit(31)

        if arg1_c > 1 or arg2_c > 1 or arg3_c > 1 or ins_c != 1:
            exit(31)
        if arg1_c == 1 and arg2_c == 0 and arg3_c == 1:
            exit(31)

        for j in range(0, 5):
            try:
                typ = child.find('arg{}'.format(i)).attrib['type']
                if typ != 'var' and typ != 'string' and typ != 'int' and typ != 'label' and typ != 'bool' and typ != 'type':
                    exit(32)
                sub_arr.append(child.find('arg{}'.format(i)).attrib['type'])
                sub_arr.append(child.find('arg{}'.format(i)).text)
                i = i + 1
            except AttributeError:
                break
            except KeyError:
                exit(31)
        arr.append(sub_arr)
    return arr


def main():

    arr = parse_xml()
    print(arr)
    s = State(arr)
    State.interpret(s)



if __name__ == "__main__":
    main()
