from Styling import Colours


# No override of colours required for TNP colours
class TNPColour(Colours.Colour):
    def __init__(self):
        super().__init__()
