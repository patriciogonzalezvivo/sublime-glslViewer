# Author @patriciogv - 2015
# http://patriciogonzalezvivo.com

import sublime, sublime_plugin, os, subprocess

version = "0.1.0"

def openShader(shaderFile):
    if shaderFile.endswith('.frag') or shaderFile.endswith('.fs'):
        settings = sublime.load_settings('glslViewer.sublime-settings')
        path = settings.get('path')
        arg = [path+'glslViewer', shaderFile]
        subprocess.Popen(arg)    

class GlslViewerCommand(sublime_plugin.EventListener):
    def on_load(self,view):
        openShader(view.file_name())

class openshaderCommand(sublime_plugin.WindowCommand):
    def run(self):
        openShader(self.window.active_view().file_name())
        
