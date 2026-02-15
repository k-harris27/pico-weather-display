import tkinter as tk
import PIL.Image
import PIL.ImageTk
import PIL.ImageDraw
import PIL.ImageFont

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 30, 30)
GREEN = (30, 255, 30)
BLUE = (30, 30, 255)
ORANGE = (200, 170, 10)
YELLOW = (170, 200, 10)

class LocalDisplay:

    def __init__(self):
        self.width = 800
        self.height = 480

        self.root = tk.Tk()
        self.root.title("Tkinter Test")
        self.root.geometry(f"{self.width}x{self.height}")

        self._image_pil = PIL.Image.new(mode="RGB", size=(self.width, self.height), color=(255,255,255))
        self._image_draw = PIL.ImageDraw.Draw(self.image_pil)

    def set_pen(self, pen):
        self.pen = pen

    def set_font(self, font: str):
        # TODO: Implement
        pass

    def pixel(self, x, y):
        self._image_draw.point((x, y), fill=self.pen)

    def clear(self):
        self._image_draw.rectangle((0,0, self.width, self.height), fill=self.pen)

    def update(self):
        image_tk = PIL.ImageTk.PhotoImage(self._image_pil)
        panel = tk.Label(self.root, image=image_tk)
        panel.image = image_tk
        panel.pack()
        self.root.mainloop()

if __name__ == "__main__":
    image_pil = PIL.Image.new(mode="RGB", size=(WIDTH, HEIGHT), color=(255,255,255))

    font_large = PIL.ImageFont.truetype("arial.ttf", 5*6)
    image_draw = PIL.ImageDraw.Draw(image_pil)
    image_draw.text((50, 50), "Hello World", fill=(0,0,0), font=font_large)

    image_tk = PIL.ImageTk.PhotoImage(image_pil)
    panel = tk.Label(root, image=image_tk)
    panel.image = image_tk
    panel.pack()

    root.mainloop()