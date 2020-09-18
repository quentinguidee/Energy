class Color:
    def __init__(self, red: int = 0, green: int = 0, blue: int = 0):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        return "rgb(" + str(self.red) + "," + str(self.green) + "," + str(self.blue) + ")"

    @staticmethod
    def from_8_bits(red: float, green: float, blue: float) -> 'Color':
        return Color(int(red * 255), int(green * 255), int(blue * 255))

    @staticmethod
    def from_8_bits_color(color: list) -> 'Color':
        return Color.from_8_bits(color[0], color[1], color[2])
