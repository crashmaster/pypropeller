"""
The utility will execute the passed function or command in a animated [+]
propeller, and when finished, the propeller will display the success or
failure.
"""

import os
import sys
import itertools
import time
import inspect
import io
import threading
import subprocess
import abc
import datetime

import six

import console


UNBUFFERED = os.fdopen(sys.stdout.fileno(), mode="wb", buffering=0)


class ExecInPropellerResult(object):
    """
    Structure containing the result values of the propeller execution:
      - Return Value: True if successful, False otherwise
      - Exception was caught or not
      - StdOutput of the executed item
      - StdError of the executed item
      - Exception as string
      - Execution time in seconds
    """

    # Do not mix up the order of this list, otherwise You must make
    # further adjustments!
    attributes = [("exec_item", "Executed Item:", " {}\n"),
                  ("exec_time", "Execution Time:", " {:.3f}s\n"),
                  ("return_value", "Return Value:", " {}\n"),
                  ("exception", "Exception caught:", " {}\n"),
                  ("stdout", "Standard output:", "\n{}\n"),
                  ("stderr", "Standard Error:", "\n{}\n"),
                  ("exception_str", "Exception:", "\n{}\n")]

    def __init__(self, **kwargs):
        self.__result_attrs = {x[0]: (x[1], kwargs.get(x[0], None))
                               for x in ExecInPropellerResult.attributes}

    def __str__(self):
        max_len = str(max([len(x[0]) for x in self.__result_attrs.values()]))
        ret_val = ""
        for i in ExecInPropellerResult.attributes:
            value = self.__result_attrs[i[0]][1]
            ret_val += ("{:<" + max_len + "}" + i[2]).format(i[1], value)
        return ret_val

    def get_executed_item(self):
        """Return the executed item."""
        return self.__result_attrs[ExecInPropellerResult.attributes[0][0]][1]

    def get_execution_time(self):
        """Return the execution time."""
        return self.__result_attrs[ExecInPropellerResult.attributes[1][0]][1]

    def get_return_value(self):
        """Return the return value."""
        return self.__result_attrs[ExecInPropellerResult.attributes[2][0]][1]

    def got_exception(self):
        """Return whether an exception was caught, or not."""
        return self.__result_attrs[ExecInPropellerResult.attributes[3][0]][1]

    def get_stdout(self):
        """Return the stdout of the executed item."""
        return self.__result_attrs[ExecInPropellerResult.attributes[4][0]][1]

    def get_stderr(self):
        """Return the stderr of the executed item."""
        return self.__result_attrs[ExecInPropellerResult.attributes[5][0]][1]

    def get_exception(self):
        """Return the exception as string."""
        return self.__result_attrs[ExecInPropellerResult.attributes[6][0]][1]


@six.add_metaclass(abc.ABCMeta)
class ExecInPropeller(object):
    """
    The base class for the running execution in the propeller, keeps the
    state and outputs.
    """
    def __init__(self):
        self.__run_state = False
        self.__success = None
        self.__exception = None
        self.__exec_time = None

    @abc.abstractmethod
    def get_executed_item(self):
        """Return the executed item as string."""
        pass

    @abc.abstractmethod
    def get_output(self):
        """ Return both stdout and stderr for the executed item.  """
        pass

    def get_run_state(self):
        """Return True if the propeller is running, False otherwise."""
        return self.__run_state

    def _set_run_state(self, state):
        """Set the run state according the passed argument."""
        self.__run_state = state

    def get_success(self):
        """Return the exit code of the executed item."""
        return self.__success

    def _set_success(self, success):
        """Set the exit code of the executed item."""
        self.__success = success

    def exception_caugth(self):
        """
        Return True if there was an exception during execution in the
        propeller, False if everything went fine.
        """
        return True if self.__exception else False

    def get_exception(self):
        """Return the exception description for the executed item."""
        if not self.__exception:
            return None
        else:
            return self.__exception.rstrip('\n')

    def _set_exception(self, exception):
        """Store the exception, which was caught during execution."""
        self.__exception = exception

    def _set_exec_time(self, time_diff):
        """Store the execution time."""
        self.__exec_time = time_diff

    def get_exec_time(self):
        """Return the execution time."""
        return self.__exec_time.total_seconds()


class ExecFuncInPropeller(ExecInPropeller, threading.Thread):
    """
    Class for keeping track of function execution in the propeller.
    """
    def __init__(self, func, func_args):
        ExecInPropeller.__init__(self)
        threading.Thread.__init__(self)
        self.__func = func
        self.__func_args = func_args
        self.__default_output = (sys.stdout, sys.stderr)
        self.__strio_output = (io.StringIO(), io.StringIO())

    def __start_output_capture(self):
        """Redirect output to the string io."""
        (sys.stdout, sys.stderr) = self.__strio_output

    def __stop_output_capture(self):
        """Restore original state of the output generation."""
        (sys.stdout, sys.stderr) = self.__default_output

    def __exec_func(self):
        """Call the wrapped function with or without arguments."""
        if self.__func_args:
            return self.__func(*self.__func_args)
        else:
            return self.__func()

    def get_executed_item(self):
        ret_val = self.__func.__name__
        ret_val += "("
        if self.__func_args:
            for i in self.__func_args:
                if isinstance(i, str):
                    ret_val += '"' + i + '"'
                else:
                    ret_val += str(i)
                if i != self.__func_args[-1]:
                    ret_val += ", "
        ret_val += ")"
        return ret_val

    def get_output(self):
        # Force None, if data not is existent
        ret_val = []
        for i in self.__strio_output:
            tmp = i.getvalue().rstrip('\n')
            if tmp:
                ret_val.append(tmp)
            else:
                ret_val.append(None)
        return ret_val

    def run(self):
        try:
            self._set_run_state(True)
            self.__start_output_capture()
            start = datetime.datetime.now()
            if not self.__exec_func():
                self._set_success(True)
            else:
                self._set_success(False)
        except Exception as err:
            self._set_exception(str(err))
        finally:
            self._set_exec_time(datetime.datetime.now() - start)
            self._set_run_state(False)
            self.__stop_output_capture()


class ExecCmdInPropeller(ExecInPropeller, threading.Thread):
    """
    Class for keeping track of command execution in the propeller.
    """
    def __init__(self, cmd):
        ExecInPropeller.__init__(self)
        threading.Thread.__init__(self)
        self.__cmd = cmd
        self.__cmd_output = None

    def get_executed_item(self):
        return " ".join(self.__cmd)

    def get_output(self):
        # None, if data is not existent
        ret_val = []
        for i in self.__cmd_output:
            tmp = i.rstrip('\n')
            if tmp:
                ret_val.append(tmp)
            else:
                ret_val.append(None)
        return ret_val

    def run(self):
        try:
            self._set_run_state(True)
            start = datetime.datetime.now()
            proc = subprocess.Popen(self.__cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            self.__cmd_output = tuple(x.decode() for x in proc.communicate())
            if not proc.returncode:
                self._set_success(True)
            else:
                self._set_success(False)
        except Exception as err:
            self._set_exception(str(err))
        finally:
            self._set_exec_time(datetime.datetime.now() - start)
            self._set_run_state(False)


class Propeller(object):
    """
    Class for the propeller drawing itself. Furthermore it will decide which
    kind of execution (funcion or command) should be chosen.
    """
    def __init__(self, **kwargs):
        self.__executor = None
        self.__func = None
        self.__func_args = None
        self.__info_str = ""
        self.__prop_chars = ["[|]", "[/]", "[-]", "[\\]"]
        self.__stdout = kwargs.get("stdout", UNBUFFERED)
        self.__setup_info_str(kwargs)
        self.__setup_func_and_args(kwargs)
        self.__setup_executor()

    def execute(self):
        """
        Start execution and update the propeller.
        This is the only public function.
        """
        self.__executor.start()

        while self.__executor.get_run_state():
            for sign in itertools.cycle(self.__prop_chars):
                self.__propeller_print(sign)
                time.sleep(0.07)
                if not self.__executor.get_run_state():
                    break

        self.__propeller_print(self.__get_end_sign(), True)

        self.__executor.join()

        return ExecInPropellerResult(
            exec_item=self.__executor.get_executed_item(),
            return_value=self.__executor.get_success(),
            exception=self.__executor.exception_caugth(),
            stdout=self.__executor.get_output()[0],
            stderr=self.__executor.get_output()[1],
            exception_str=self.__executor.get_exception(),
            exec_time=self.__executor.get_exec_time())

    def __setup_info_str(self, kwargs):
        """Set up the information string correctly, if present."""
        info = kwargs.get("info", None)
        self.__info_str = " " + info if info and " " != info[0] else info

    def __setup_func_and_args(self, kwargs):
        """Set up function and arguments correctly."""
        func = kwargs.get("func", None)
        cmd = kwargs.get("cmd", None)
        args = kwargs.get("args", None)
        # Case, where only func was set
        if func and not cmd:
            self.__func = func
            if args and not isinstance(args, list):
                raise RuntimeError("Expected type for the arguments is list")
            self.__func_args = args
        # Case, where only cmd was set
        elif cmd and not func:
            self.__func = cmd
            self.__func_args = None
        else:
            raise RuntimeError("Incorrect parameters for the Propeller")

    def __setup_executor(self):
        """Function or command execution was requested."""
        if inspect.isfunction(self.__func) or \
           inspect.isbuiltin(self.__func) or \
           inspect.ismethod(self.__func):
            self.__executor = ExecFuncInPropeller(self.__func,
                                                  self.__func_args)
            if not self.__info_str:
                self.__info_str = " " + self.__func.__name__
        elif isinstance(self.__func, list):
            self.__executor = ExecCmdInPropeller(self.__func)
            if not self.__info_str:
                self.__info_str = " " + " ".join(self.__func)
        else:
            print("Error: function passed to Propeller is incorrect: " +
                  str(type(self.__func)))
            sys.exit(1)

    def __normalized_desc(self):
        """
        If the line won't fit into the terminal, then replace the last
        characters with ...
        """
        len_str_aft_prop = len(self.__info_str)
        len_prop_chars = max(len(x) for x in self.__prop_chars)
        len_console_line = console.get_terminal_size()[0]
        if len_str_aft_prop + len_prop_chars > len_console_line:
            return self.__info_str[:len_console_line - len_str_aft_prop -
                                   len_prop_chars - 3] + "..."
        return self.__info_str

    def __propeller_print(self, propeller, add_newline=False):
        """Print the propeller! :-)"""
        self.__stdout.write(
            ("\r%s%s" % (propeller, self.__normalized_desc())).encode())
        if add_newline:
            self.__stdout.write(b'\n')

    def __get_end_sign(self):
        """
        When the execution ends, print the end sign according the executed
        item exit code.
        """
        success = self.__executor.get_success()
        return "[%s]" % console.string_in_color(
            console.CONSOLE_FONT_ATTRIBUTE["NORMAL"],
            console.CONSOLE_FONT_BG_COLOR["DEFAULT"],
            console.CONSOLE_FONT_FG_COLOR["GREEN" if success else "RED"],
            "+" if success else "-")

# vim: set filetype=python
