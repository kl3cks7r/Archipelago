import asyncio

from kvui import GameManager
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.widget import Widget
from kivy.clock import Clock

from CommonClient import logger

from .Connector import *

class InstanceCard(MDCard):
    name = StringProperty()
    version = StringProperty()
    tweaked = BooleanProperty(False)

    def launch_instance(self):
        logger.info(f"Launching {self.name!r} (tweaked={self.tweaked})")
        launch_game(App.get_running_app().ctx, tweaked=self.tweaked) # FIXME: find a way to pass ctx to this widget

class LauncherWidget(MDBoxLayout):
    version = StringProperty("v0.0.0")
    game_path = StringProperty("")
    download_button_text = StringProperty("Download Game")
    dialog = ObjectProperty(MDDialog)

    def browse_game_path(self):
        """Stub for file-browse dialog."""
        logger.info("browse_game_path called")
        # TODO: integrate FileChooser to pick game executable

    def reveal_game_path(self):
        """Stub for revealing path in OS file manager."""
        logger.info("reveal_game_path called")
        # TODO: use platform-specific call to open folder

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
                    on_release=self.dialog.dismiss()
                ),
                MDButton(
                    MDButtonText(text="Accept"),
                    style="text",
                    on_release=self.dialog_confirm()
                ),
                spacing="8dp",
            ),
        )
        self.dialog.open()
        logger.info("add_instance called")
    
    def dialog_confirm(self):
        """Handle dialog confirmation."""
        self.dialog.dismiss()
        logger.info("Dialog confirmed, starting download")

    def update_instances_panel(self):
        """Stub for refreshing instance list from model."""
        logger.info("update_instances_panel called")
        # TODO: iterate over your instance store and update UI rows


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

        # Clock.schedule_interval(self.update_instances_panel, 0.5) Update the instances panel after the UI is built

        return container

def start_gui(ctx):
    ctx.ui = CaveStoryManager(ctx)
    ctx.ui_task = asyncio.create_task(ctx.ui.async_run(), name="UI")