# Author @patriciogv - 2015
# http://patricio.io

import sublime, sublime_plugin, os, subprocess

version = "0.2.0"
process = {}

def openShader(shaderFile):
    if shaderFile.endswith('.frag') or shaderFile.endswith('.fs'):
        settings = sublime.load_settings('glslViewer.sublime-settings')
        path = settings.get('path')
        view = sublime.active_window().active_view()
        texturesLines = view.find_all('uniform sampler2D ')
        if len(texturesLines) > 0:
            sublime.message_dialog('This shader use ' + str(len(texturesLines)) + ' textures. So far this textures can not be loaded, we are working to support this in future versions. Thank you.')

        arg = [path+'glslViewer', shaderFile]
        process[shaderFile] = subprocess.Popen(arg)

class GlslViewerCommand(sublime_plugin.EventListener):
    def on_load(self,view):
        openShader(view.file_name())
    def on_activated(self,view):
        shaderFile = view.file_name()
        if shaderFile in process:
            if process[shaderFile].poll() is not None:
                openShader(shaderFile)

    def on_close(self,view):
        shaderFile = view.file_name()
        sublime.message_dialog('kill '+shaderFile)
        if shaderFile in process:
            process[shaderFile].kill()
            del process[shaderFile]

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
