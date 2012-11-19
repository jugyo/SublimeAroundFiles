import sublime, sublime_plugin
import os

class AroundFilesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        dirname = os.path.dirname(self.view.file_name())
        self.around_file(dirname)

    def around_file(self, dirname):
        files = os.listdir(dirname)
        files = map(lambda f: os.path.join(dirname, f), files)
        files = filter(lambda f: f != self.view.file_name(), files)

        def on_done(index):
            if index < 0:
              return
            file = files[index]
            if os.path.isdir(file):
              self.around_file(file)
            else:
              self.view.window().open_file(file)

        items = []
        for file in files:
            _file = file
            for folder in sublime.active_window().folders():
              _file = file.replace(folder + '/', '', 1)
            if os.path.isdir(file):
                items.append(_file + '/')
            else:
                items.append(_file)
        self.view.window().show_quick_panel(items, on_done)
