# Author @patriciogv - 2015
# http://patriciogonzalezvivo.com
import sublime, sublime_plugin, os, subprocess

class OpenshaderCommand(sublime_plugin.EventListener):
    def on_load(self,view):
        f = view.file_name()
        if f.endswith('.frag') or f.endswith('.fs'):
            arg = ['glslViewer', view.file_name()]
            subprocess.Popen(arg)
