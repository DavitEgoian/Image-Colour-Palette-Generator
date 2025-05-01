from PIL import Image, ImageDraw

class PaletteSaver:
    def __init__(self, colors: list[tuple[int, int, int]], swatch_size: tuple[int, int] = (60, 60)) -> None:
        self.colors = colors
        self.swatch_size = swatch_size

    def save(self, path: str) -> None:
        w, h = self.swatch_size
        img = Image.new('RGB', (w * len(self.colors), h))
        draw = ImageDraw.Draw(img)
        for i, color in enumerate(self.colors):
            draw.rectangle([i * w, 0, (i + 1) * w, h], fill=color)
        img.save(path)