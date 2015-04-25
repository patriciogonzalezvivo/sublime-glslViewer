# Author @patriciogv - 2015
# http://patricio.io

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

class glsltemplateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "\
#ifdef GL_ES\n\
precision mediump float;\n\
#endif\n\
\n\
uniform float u_time;\n\
uniform vec2 u_mouse;\n\
uniform vec2 u_resolution;\n\
\n\
void main (void) {\n\
    vec2 st = gl_FragCoord.xy/u_resolution.xy;\n\
    vec3 color = vec3(st,0.0);\n\
\n\
\n\
    gl_FragColor = vec4(color,1.0);\n\
}\n")

class newshaderCommand(sublime_plugin.WindowCommand):
    def run(self):
        newView = self.window.new_file()
        newView.run_command('glsltemplate')




        
