import asyncio

from kvui import GameManager
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.widget import Widget
from kivy.clock import Clock

from CommonClient import logger

from .. import CaveStoryWorld

from .Connector import *
from .Patcher import patch_mychar

class InstanceCard(MDCard):
    name = StringProperty()
    version = StringProperty()
    char = StringProperty("Select")
    tweaked = BooleanProperty(False)

    def launch_instance(self):
        ctx = App.get_running_app().ctx
        ctx.tweaked = self.tweaked
        logger.info(f"Launching {self.name!r} (tweaked={self.tweaked})")
        launch_game(ctx, tweaked=self.tweaked)
    
    def open_menu(self, item):
        menu_items = [
            {
                "text": char,
                "on_release": lambda x=char: self.menu_callback(x),
            } for char in CS_MYCHAR
        ]
        MDDropdownMenu(caller=item, items=menu_items).open()

    def menu_callback(self, text_item):
        self.char = text_item
        game_dir = Path(CaveStoryWorld.settings['game_dir']).expanduser()
        patch_mychar(game_dir, self.char)
        logger.info(f"Character set to {self.char!r}")

class LauncherWidget(MDBoxLayout):
    dialog = ObjectProperty(MDDialog)
    instances_dir = StringProperty(CaveStoryWorld.settings['game_dir'])

    def browse_game_path(self):
        """Stub for file-browse dialog."""
        new_folder = CaveStoryWorld.settings['game_dir'].browse()
        if new_folder is not None:
            
            Clock.schedule_once(lambda dt: setattr(self, 'instances_dir', new_folder), 0)
            CaveStoryWorld.settings['game_dir'] = new_folder
            logger.info(f"New game path selected: {CaveStoryWorld.settings['game_dir']!r}")

    def add_instance(self):
        """Stub for adding a new game instance row."""
        self.dialog = MDDialog(
            MDDialogIcon(
                icon="download",
            ),
            MDDialogHeadlineText(
                text="Third-Party Software Notice",
            ),
            MDDialogSupportingText(
                text="This launcher will automatically download the required Cave Story Randomizer project, which is not affiliated with Archipelago.",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Cancel"),
                    style="text",
                    on_release=self._on_cancel
                ),
                MDButton(
                    MDButtonText(text="Accept"),
                    style="text",
                    on_release=self._on_confirm
                ),
                spacing="8dp",
            ),
        )
        self.dialog.open()
        logger.info("add_instance called")

    def _on_cancel(self, *args):
        self.dialog.dismiss()
    def _on_confirm(self, *args):
        logger.info("Dialog confirmed, starting download")
        self.dialog.dismiss()


class CaveStoryManager(GameManager):
    logging_pairs = [
        ("Client", "Archipelago")
    ]
    base_title = "Cave Story Client"
    instances_panel: Optional[LauncherWidget] = None

    def __init__(self, ctx) -> None:
        super().__init__(ctx)
    
    def build(self):
        container = super().build()
        panel = self.add_client_tab("Cave Story Launcher", ScrollView())

        self.instances_panel = LauncherWidget()
        panel.content.add_widget(self.instances_panel)

        return container

def start_gui(ctx):
    ctx.ui = CaveStoryManager(ctx)
    ctx.ui_task = asyncio.create_task(ctx.ui.async_run(), name="UI")
    import pkgutil
    data = pkgutil.get_data(CaveStoryWorld.__module__, "CaveStoryClient/CaveStoryGui.kv").decode()
    Builder.load_string(data)