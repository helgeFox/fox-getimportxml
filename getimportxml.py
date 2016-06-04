import sublime, sublime_plugin, sys, os

from suds.client import Client

class ShowContentsCommand(sublime_plugin.TextCommand):
  def run(self, edit, content):
    for region in self.view.sel():
      self.view.replace(edit, region, content)

class getimportxmlCommand(sublime_plugin.TextCommand):

  url = 'http://ws.prod.stage.foxpublish.net/EditorService.asmx?WSDL'
  edit = None

  def is_enabled(self):
    return True

  def run(self, edit):
    self.edit = edit
    caption = "Set sessionid"
    initial_text = "<paste your session id here!>"
    panel = self.view.window().show_input_panel (
      caption, 
      initial_text, 
      self.on_panel_done,
      self.on_panel_change,
      self.on_cancel)

  def on_panel_done(self, sessionid):
    if sessionid:
      client = Client(self.url)
      result = client.service.GetImportXml(sessionid)
      self.show_result(result)

  def show_result(self, content):
    view = sublime.active_window().new_file()
    view.run_command('show_contents', {"content": content.Xml})
    view.run_command('fox_cleanup_xml')

  def on_panel_change(self, abbr):
    if abbr:
      print ("Input panel changed... (" + abbr + ")")
      return

  def on_cancel(self, abbr):
    print ('GetImportXml cancelled')
    return
