"""
:module: 
:synopsis: "Kurzbeschreibung"
:author: Julien Wagler
    
public functions
-----------------

.. autofunction:: "Name der Funktion"


private functions
------------------

.. autofunction:: "Name der Funktion"



"""

from kivy.app import App
from kivy.uix.widget import Widget


class PongGame(Widget):
    pass


class PongApp(App):

    def build(self):
        return PongGame()


if __name__ == '__main__':
    PongApp().run()
