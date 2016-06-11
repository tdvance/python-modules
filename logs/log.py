from collections import Iterable
from datetime import datetime
import os
import textwrap
import traceback

class Log:
    def __init__(self):
        self._file_levels = dict()
        self._default_levels = set(['critical', 'info'])
        
    def set_file_levels(self, files, levels, trunc=True):
        """For each file or stream in files, associate all levels in levels.
Subsequent logging to those levels will go to those files.  If trunc
is true, any files (but not streams) will be created or truncated by
this call.  The 'unconditional' level is assumed for all files.

        """
        for file in files:
            self._file_levels[file] = set(levels)
            self._file_levels[file].add('unconditional')
            if Log._is_path(file):
                open(file, 'wt').close()

    def get_files(self):
        """Generate all files or streams currently being logged to.

        """
        for file in self._file_levels:
            yield file
            
    def set_default_levels(self, *levels):
        """Set the default levels to log to when no levels are specified.

        """
        self._default_levels = set(levels)

    def get_default_levels(self):
        """Generate the current default levels.
        
        """
        for level in self._default_levels:
            yield level
    
    def stop_logging(self, *files):
        """Stop all logging to the specified files, including 'unconditional'
        levels.

        """
        for file in files:
            self._file_levels.pop(file, None)
    
    def log(self, fmt, *args, levels=None, end=os.linesep):
        """Log the printf-like fmt and args to all registered files and
        streams having levels among those specified (collection or
        single string), or default if none are specified.  end
        specifies an alternate end-of-line character.  If
        unconditional is among the levels, all registered files and
        streams are logged to.

        """
        ll = levels
        if levels is None:
            ll = [l for l in self.get_default_levels()]
        else:
            ll = [l for l in Log._flatten(ll)]
        for f in self.get_files():
            self._print(Log._get_date(), fmt, *args, file=f, levels=ll, end=end)
        exit()
    def log_display(self, fmt, *args, levels=None, end=os.linesep, star='*', width=50):
        """Log the printf-like fmt and args to all registered files and
        streams having levels among those specified (collection or
        single string), or default if none are specified.  end
        specifies an alternate end-of-line character.  If
        unconditional is among the levels, all registered files and
        streams are logged to.

        In addition, set the log entry apart with lines of stars and
        blank lines for easy visibility, and word-wrap log lines.

        """
        ll = levels
        if levels is None:
            ll = self.get_default_levels()
        else:
            ll = [l for l in Log._flatten(ll)]
        stars = star*width
        blank = ' '*width
        lines = textwrap.wrap(fmt % tuple(args), width=width)
        for i in range(len(lines)):
            if len(lines[i]) < width:
                lines[i] += ' '*(width - len(lines[i]))
            lines[i] = '* ' + lines[i] + ' *'
        lines = [blank, stars] + lines + [stars, blank]
        for f in self.get_files():
            for line in lines:
                self._print(Log._get_date(), line, file=f, levels=ll, end=end)

    def log_critical(self, fmt, *args, end=os.linesep):
        """
        Same as self.log(fmt, *args, levels='critical', end=end)
        """
        self.log(fmt, *args, levels='critical', end=end)
    
    def log_info(self, fmt, *args, end=os.linesep):
        """
        Same as self.log(fmt, *args, levels='info', end=end)
        """        
        self.log(fmt, *args, levels='info', end=end)

    def log_verbose(self, fmt, *args, end=os.linesep):
        """
        Same as self.log(fmt, *args, levels='verbose', end=end)
        """
        self.log(fmt, *args, levels='verbose', end=end)
    
    def log_debug(self, fmt, *args, end=os.linesep):
        """Same as self.log(fmt, *args, levels='debug', end=end), except
        information on the location in the code is also printed.

        """        
        self.log(fmt, *args, levels='debug', end=end)
        t = traceback.extract_stack()[-2]
        source = t[0]
        line = t[1]
        function = t[2]
        self.log("  ... at %s:%d in %s", source, line, function)

    def log_warn(self, fmt, *args, end=os.linesep):
        """
        Same as self.log(fmt, *args, levels='unconditional', end=end)
        """        
        self.log(fmt, *args, levels='unconditional', end=end)

    def log_die(self, fmt, *args, exception=None, exc_arg="", end=os.linesep):
        """Same as self.log(fmt, *args, levels='unconditional', end=end),
        followed by raising exception(exc_arg) if specified, followed
        by exit().

        """                
        self.log(fmt, *args, levels='unconditional', end=end)
        if exception is not None:
            raise exception(exc_arg)
        exit()

    def _print(self, date, fmt, *args, file, levels, end):
        if (set(levels) & set(self._file_levels[file])):
            if Log._is_path(file):
                out = open(file, 'at')
            else:
                out = file            
            print(date + fmt % tuple(args), list(levels), file=out, end=end)
            if out != file:
                out.close()
    
    @staticmethod
    def _flatten(arg, ignore_types=(str, bytes)):
        for x in arg:
            if isinstance(x, Iterable) and not isinstance(x, ignore_types):
                yield from Log._flatten(x, ignore_types)
            else:
                yield x

    @staticmethod
    def _is_stream(arg):
        return has_attr(arg, 'write')

    @staticmethod
    def _is_path(arg):
        return isinstance(arg, str)

    @staticmethod
    def _get_date():
        return datetime.now().strftime("%F %T ")
    
