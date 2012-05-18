import sublime
import sublime_plugin
import re

class CssformatCommand(sublime_plugin.TextCommand):

    def unify(self, str):
        str = str.replace('\r\n', '\n').replace('\r', '\n')
        
        indent_characters = '\t'
        if self.view.settings().get('translate_tabs_to_spaces'):
            indent_characters = ' ' * int(settings.get('tab_size', 4))

        str = indent_characters.join(str.split('\t'))

        str = re.compile(r'\s*{\s*').subn(r' {\n' + indent_characters, str)[0]
        str = re.compile(r';\s*').subn(r';\n' + indent_characters, str)[0]
        str = re.compile(r',\s*').subn(r', ', str)[0]
        str = re.compile(r'\s*}').subn(r'}\n', str)[0]
        str = re.compile(r'}\s*(.+)').subn(r'}\n\1', str)[0]
        str = re.compile(r'\n\s*([^{\n]+):\s*').subn(r'\n' + indent_characters + r'\1: ', str)[0]
        str = re.compile(r'([A-z0-9\)])}').subn(r'\1;\n}', str)[0]

        line_endings = self.view.settings().get('default_line_ending')
        if line_endings == 'windows':
            str = str.replace('\n', '\r\n')
        elif line_endings == 'mac':
            str = str.replace('\n', '\r')
        
        return str

    def run(self, edit):
        sublime.status_message('CSSformating...')
        edit = self.view.begin_edit('CSSformat')
        
        for sel in self.view.sel():
                str = self.unify(self.view.substr(sel))
                self.view.replace(edit, sel, str)    

        self.view.end_edit(edit)
        sublime.status_message('CSS file is formated successfully')
