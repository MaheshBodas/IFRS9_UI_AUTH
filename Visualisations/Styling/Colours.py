from abc import ABC


class Colour(ABC):
    def __init__(self):
        self.__theme1 = {0: "#13245A", 1: "#BCCAF1", 2: "#7A95E2", 3: "#375FD5", 4: "#0E1C43", 5: "#0A122C"}
        self.__theme2 = {0: "#7E99AA", 1: "#E4EAED", 2: "#CBD6DC", 3: "#B1C1CB", 4: "#587485", 5: "#3A4E58"}
        self.__theme3 = {0: "#599FE1", 1: "#DDECF9", 2: "#BCD9F3", 3: "#9AC6ED", 4: "#247AC8", 5: "#185285"}
        self.__theme4 = {0: "#5A713B", 1: "#DFE8D2", 2: "#BED0A6", 3: "#9EB979", 4: "#43542C", 5: "#2D381D"}
        self.__theme5 = {0: "#DEB43F", 1: "#F9EFD7", 2: "#F1E0B1", 3: "#EBD08B", 4: "#B68C1F", 5: "#795E15"}
        self.__theme6 = {0: "#A13B00", 1: "#FFD3B9", 2: "#FFA873", 3: "#FF7B2D", 4: "#792E00", 5: "#511F00"}
        self.__theme_white = {0: "#FFFFFF", 1: "#F2F2F2", 2: "#D9D9D9", 3: "#BFBFBF", 4: "#A6A6A6", 5: "#808080"}
        self.__theme_black = {0: "#000000", 1: "#808080", 2: "#595959", 3: "#404040", 4: "#A6A6A6", 5: "#808080"}
        self.__theme_l_grey = {0: "#EBEBEB", 1: "#D2D2D2", 2: "#AFAFAF", 3: "#757575", 4: "#3A3A3A", 5: "#0D0D0D"}
        self.__theme_d_grey = {0: "#949494", 1: "#E9E9E9", 2: "#D3D3D3", 3: "#BEBEBE", 4: "#6F6F6F", 5: "#494949"}
        self.__green = "#9EB979"
        self.__amber = "#DEB43F"
        self.__yellow = "#EBD08B"
        self.__red = "#A13B00"

        self.__theme = {1: self.__theme1, 2: self.__theme2, 3: self.__theme3, 4: self.__theme4, 5: self.__theme5,
                        6: self.__theme6}
        self.__RAYG = {"Red": self.__red, "Amber": self.__amber, "Yellow": self.__yellow, "Green": self.__green}
        self.__font = "Trebuchet MS"

    @property
    def font(self):
        return self.__font

    def get_theme_colour(self, accent_colour: int, shade: int) -> str:

        if accent_colour > 6 or shade > 5 or accent_colour < 0 or shade < 0:
            raise Exception("Invalid theme colour, accent colour should be between 0 and 6 and shade between 0 and 5")

        col = self.__theme[accent_colour]
        return col[shade]

    def get_RAYG(self, RAYG: str) -> str:

        if RAYG not in ["Red", "Amber", "Yellow", "Green"]:
            raise Exception("Invalid RAYG colour, should be either 'Red', 'Amber', 'Yellow' or 'Green'")

        return self.__RAYG[RAYG]

    def get_black(self, shade: int) -> str:
        if shade > 5 or shade < 0:
            raise Exception("Invalid shade, it should be between 0 and 5")

        return self.__theme_black[shade]

    def get_white(self, shade: int) -> str:
        if shade > 5 or shade < 0:
            raise Exception("Invalid shade, it should be between 0 and 5")

        return self.__theme_white[shade]

    def get_light_grey(self, shade: int) -> str:
        if shade > 5 or shade < 0:
            raise Exception("Invalid shade, it should be between 0 and 5")

        return self.__theme_l_grey[shade]

    def get_dark_grey(self, shade: int) -> str:
        if shade > 5 or shade < 0:
            raise Exception("Invalid shade, it should be between 0 and 5")

        return self.__theme_d_grey[shade]
