# Author @patriciogv - 2015
# http://patricio.io

import sublime, sublime_plugin, os, subprocess, sys, re

version = "0.4.0"

def openShader(view):
    shaderFile = view.file_name()
    settings = sublime.load_settings('glslViewer.sublime-settings')
    if settings.get('auto-start'):
        if shaderFile.endswith('.frag') or shaderFile.endswith('.fs'):
            cmd = []
            cmd.append(settings.get('path')+'glslViewer')
            cmd.append(shaderFile)
            os.chdir(os.path.dirname(shaderFile))
            if len(view.find_all('uniform sampler2D')) > 0:
                fp = open(shaderFile)
                textures = []
                images = []
                default = "*.png"
                for file in os.listdir(os.getcwd()):
                    if file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".png") or file.endswith(".PNG"):
                        default = file
                        break
                while 1:
                    line = fp.readline()
                    if not line:
                        break
                    result = re.search(r'(uniform)\s+(sampler2D)\s+(\w*)', line)
                    if result != None:
                        textures.append(result.group(3))
                def askForTexture(i):
                    def done(filename):
                        cmd.append('--'+textures[i])
                        cmd.append(os.path.abspath(filename))
                        if textures[i] == textures[-1]:
                            view.window().run_command('exec',{'cmd':cmd})
                        else:
                            askForTexture(i+1)
                    def cancel():
                        return
                    view.window().show_input_panel("Load "+textures[i]+" width: ", default, done, None, cancel)

                askForTexture(0)
            else:
                view.window().run_command('exec',{'cmd':cmd})


class GlslViewerCommand(sublime_plugin.EventListener):
    def on_load(self,view):
        openShader(view)

class openshaderCommand(sublime_plugin.WindowCommand):
    def run(self):
        openShader(self.window.active_view())

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
