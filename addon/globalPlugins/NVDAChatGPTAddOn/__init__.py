import globalPluginHandler
import wx
import globalPluginHandler
import ui
import gui
import config
from logHandler import log
from scriptHandler import script
from .interface import ChatGPTInterface

ADDON_SUMMARY = _("NVDA Add-on for ChatGPT")

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    """
    Implementing global plugin for the addon
    """
    def __init__(self):

        # initial setup for global plugin
        super(GlobalPlugin, self).__init__()
        self.chatgpt = ChatGPTInterface
        # create menu item to add to NVDA menu
        self.createMenu()
    
    def createMenu(self):
        # menu item is created in NVDA's tool menu
        tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
        self.menu_item = tools_menu.Append(wx.ID_ANY, _("ChatGPT Addon"))
        gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onChatGPTDialog, self.menu_item)

    def onChatGPTDialog(self, evt):
        # Open ChatGPT dialog
        wx.CallAfter(self.showChatGPTDialog)
    
    def showChatGPTDialog(self):
        # Create and show ChatGPT dialog
        dialog = ChatGPTDialog(gui.mainFrame)
        dialog.ShowModal()
        dialog.Destroy()
    
    @script(
        description=_("Opens ChatGPT Addon dialog"),
        gesture="kb:NVDA+shift+c"
    )
    def script_openChatGPTDialog(self, gesture):
        wx.CallAfter(self.showChatGPTDialog)
        
    def terminate(self):
        """Clean up when add-on is disabled or uninstalled."""
        try:
            tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
            tools_menu.Remove(self.menu_item)
        except:
            pass
        super(GlobalPlugin, self).terminate()

class ChatGPTDialog(wx.Dialog):
    def __init__(self, parent):
        super(ChatGPTDialog, self).__init__(
            parent,
            title=_("ChatGPT Assistant"),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        
        self.chatgpt = ChatGPTInterface()

        # # Get the global plugin instance to access the ChatGPT interface
        # for plugin in globalPluginHandler.runningPlugins:
        #     if isinstance(plugin, GlobalPlugin):
        #         self.chatgpt = plugin.chatgpt
        #         break
        # else:
        #     # Fallback if plugin instance not found
        #     self.chatgpt = ChatGPTInterface()
        
        # Create dialog layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Input field label
        input_label = wx.StaticText(self, label=_("Enter your question:"))
        main_sizer.Add(input_label, flag=wx.ALL, border=10)
        
        # Input text field
        self.input_field = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        self.input_field.SetMinSize((400, 100))
        main_sizer.Add(self.input_field, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        
        # Response field label
        response_label = wx.StaticText(self, label=_("Response:"))
        main_sizer.Add(response_label, flag=wx.ALL, border=10)
        
        # Response text field (read-only)
        self.response_field = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.response_field.SetMinSize((400, 200))
        main_sizer.Add(self.response_field, proportion=2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        
        # Buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.submit_button = wx.Button(self, label=_("Submit"))
        self.submit_button.Bind(wx.EVT_BUTTON, self.onSubmit)
        button_sizer.Add(self.submit_button, flag=wx.RIGHT, border=10)
        
        self.settings_button = wx.Button(self, label=_("Settings"))
        self.settings_button.Bind(wx.EVT_BUTTON, self.onSettings)
        button_sizer.Add(self.settings_button, flag=wx.RIGHT, border=10)
        
        close_button = wx.Button(self, wx.ID_CLOSE, _("Close"))
        close_button.Bind(wx.EVT_BUTTON, self.onClose)
        button_sizer.Add(close_button)
        
        main_sizer.Add(button_sizer, flag=wx.ALL | wx.ALIGN_RIGHT, border=10)
        
        self.SetSizer(main_sizer)
        self.SetEscapeId(wx.ID_CLOSE)
        
        # Set focus to input field when dialog opens
        self.input_field.SetFocus()
        
        # Bind enter key in input field
        self.input_field.Bind(wx.EVT_TEXT_ENTER, self.onSubmit)
        
        # Size the dialog
        self.Fit()
        self.SetMinSize(self.GetSize())
        
    def onSubmit(self, evt):
        # Process the user's query
        query = self.input_field.GetValue()
        if not query.strip():
            # Translators: Message shown when no query is entered
            ui.message(_("Please enter a question"))
            return
        
        # Check if API key is set
        if not self.chatgpt.api_key:
            ui.message(_("API key not set. Please configure in settings."))
            return
        
        # Show processing message
        ui.message(_("Processing your query..."))
        self.response_field.SetValue(_("Waiting for response..."))
        
        # Make the API call and get response
        response = self.chatgpt.send_query(query)
        self.response_field.SetValue(response)
        
        # Announce that response is ready
        ui.message(_("Response received"))
    
    def onSettings(self, evt):
        # Open settings dialog
        dialog = SettingsDialog(self, self.chatgpt)
        dialog.ShowModal()
        dialog.Destroy()
        
    def onClose(self, evt):
        self.EndModal(wx.ID_CLOSE)


class SettingsDialog(wx.Dialog):
    def __init__(self, parent, chatgpt_interface):
        super(SettingsDialog, self).__init__(
            parent,
            title=_("ChatGPT Assistant Settings"),
            style=wx.DEFAULT_DIALOG_STYLE
        )
        
        self.chatgpt = chatgpt_interface
        
        # Create dialog layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # API Key
        api_key_sizer = wx.BoxSizer(wx.HORIZONTAL)
        api_key_label = wx.StaticText(self, label=_("API Key:"))
        self.api_key_field = wx.TextCtrl(self, value=self.chatgpt.api_key)
        api_key_sizer.Add(api_key_label, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=10)
        api_key_sizer.Add(self.api_key_field, proportion=1, flag=wx.EXPAND)
        main_sizer.Add(api_key_sizer, flag=wx.EXPAND | wx.ALL, border=10)
        
        # Model selection
        model_sizer = wx.BoxSizer(wx.HORIZONTAL)
        model_label = wx.StaticText(self, label=_("Model:"))
        self.model_choice = wx.Choice(self, choices=["gpt-3.5-turbo", "gpt-4"])
        # Set the current model
        if self.chatgpt.model == "gpt-4":
            self.model_choice.SetSelection(1)
        else:
            self.model_choice.SetSelection(0)
        model_sizer.Add(model_label, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=10)
        model_sizer.Add(self.model_choice, flag=wx.EXPAND)
        main_sizer.Add(model_sizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        
        # Max tokens
        max_tokens_sizer = wx.BoxSizer(wx.HORIZONTAL)
        max_tokens_label = wx.StaticText(self, label=_("Max Tokens:"))
        self.max_tokens_field = wx.SpinCtrl(self, min=100, max=4000, initial=self.chatgpt.max_tokens)
        max_tokens_sizer.Add(max_tokens_label, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=10)
        max_tokens_sizer.Add(self.max_tokens_field, flag=wx.EXPAND)
        main_sizer.Add(max_tokens_sizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        
        # Buttons
        buttons_sizer = wx.StdDialogButtonSizer()
        self.save_button = wx.Button(self, wx.ID_OK, _("Save"))
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, _("Cancel"))
        self.save_button.SetDefault()
        buttons_sizer.AddButton(self.save_button)
        buttons_sizer.AddButton(self.cancel_button)
        buttons_sizer.Realize()
        main_sizer.Add(buttons_sizer, flag=wx.EXPAND | wx.ALL, border=10)
        
        self.SetSizer(main_sizer)
        self.Fit()
        
        # Bind events
        self.save_button.Bind(wx.EVT_BUTTON, self.onSave)
        
    def onSave(self, evt):
        # Update settings
        self.chatgpt.api_key = self.api_key_field.GetValue()
        self.chatgpt.model = self.model_choice.GetString(self.model_choice.GetSelection())
        self.chatgpt.max_tokens = self.max_tokens_field.GetValue()
        
        # Save settings to file
        self.chatgpt.save_settings()
        
        # Close dialog
        self.EndModal(wx.ID_OK)