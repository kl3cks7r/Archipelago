import asyncio

from kvui import GameManager
from kivy.clock import Clock
from kivy.lang import Builder

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

from .Connector import *

class CaveStoryManager(GameManager):
    logging_pairs = [
        ("Client", "Archipelago")
    ]
    base_title = "Cave Story Client"
    settings_panel: Optional[BoxLayout] = None
    cs_button: Optional[Button] = None

    def __init__(self, ctx) -> None:
        super().__init__(ctx)
    
    def build(self):
        container = super().build()

        panel = self.add_client_tab("Cave Story Launcher", ScrollView())
        self.settings_panel = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40),
        )
        panel.content.add_widget(self.settings_panel)

        Clock.schedule_once(self.add_cs_gui, 0)

        return container
    
    def add_cs_gui(self, _dt):
        if self.ctx.game_platform == 'freeware':
            self.cs_button = Button(text="Launch Cave Story Freeware")
        elif self.ctx.game_platform == 'tweaked':
            self.cs_button = Button(text="Launch Cave Story Tweaked")
        self.cs_button.bind(on_press=lambda inst: launch_game(self))
        self.settings_panel.add_widget(self.cs_button)



def start_gui(ctx):
    """
    Starts the GUI for the Cave Story client.
    :param ctx: The context containing settings and other necessary information.
    """
    """Import kivy UI system and start running it as self.ui_task."""
    
    ctx.ui = CaveStoryManager(ctx)
    ctx.ui_task = asyncio.create_task(ctx.ui.async_run(), name="UI")