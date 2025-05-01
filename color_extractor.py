from PIL import Image
from collections import Counter

class ColorExtractor:
    def __init__(self, image: Image.Image) -> None:
        self.image = image

    def top_colors(self, num: int = 10) -> list[tuple[int, int, int]]:
        pixels = self.image.convert('RGB').getdata()
        counter = Counter(pixels)
        return [color for color, _ in counter.most_common(num)]