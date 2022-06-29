from tkinter import *
import pyautogui as pg

WIDTH, HEIGHT = pg.size()


class SS():
    def __init__(self):
        #window config
        self.root = Tk()
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.attributes("-alpha", 0.3)
        self.root.overrideredirect(True)
        self.root.config(bg="black")
        self.root.attributes("-transparentcolor", "red")

        #bind actions
        self.root.bind("<FocusOut>", self.close)
        self.root.bind("<ButtonRelease-3>", self.close)
        self.root.bind("<Escape>", self.close)

        self.root.bind("<Button-1>", self.on_start)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<ButtonRelease-1>", self.on_stop)

        #util vars
        self.x_start = 0
        self.y_start = 0
        self.s_width = 0
        self.s_height = 0

        
        self.root.mainloop()

    def close(self, e = None):
        self.root.destroy()

    def on_start(self, e):
        self.init_xy = (e.x_root, e.y_root)

    def on_drag(self, e):
        try:
            self.selection.destroy()
        except:
            pass
        self.current_xy = (e.x_root, e.y_root)
        self.w, self.h = (abs(self.init_xy[0]-self.current_xy[0]), abs(self.init_xy[1]-self.current_xy[1]))

        if self.current_xy[0] < self.init_xy[0]:
            self.x_start = self.current_xy[0]
        else:
            self.x_start = self.init_xy[0]
        if self.current_xy[1] < self.init_xy[1]:
            self.y_start = self.current_xy[1]
        else:
            self.y_start = self.init_xy[1]

        self.selection = Label(self.root, bg="red")
        self.selection.place(x=self.x_start, y=self.y_start, width=self.w, height=self.h)

    def on_stop(self, e):
        self.end_xy = (e.x_root, e.y_root)
        self.screenshot()
        self.close()

    def screenshot(self):
        img = pg.screenshot(region=(self.x_start, self.y_start, self.w, self.h))
        img.save("ss.png")
        #todo: handle image properly


if __name__ == "__main__":
    SS()