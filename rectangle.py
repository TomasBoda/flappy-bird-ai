
class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # funckia, ktorá vyhodnotí, či sa dva obdĺžniky prekrývajú:
    # slúži na výpočet kolízí vtáka s potrubím
    def intersects(self, rect) -> bool:
        if self.x + self.width >= rect.x and self.x <= rect.x + rect.width and self.y + self.height >= rect.y and self.y <= rect.y + rect.height:
            return True

        return False