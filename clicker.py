from common_utils import Point

import matplotlib.pyplot as plt
import math
import time


class CoordSelector:
    def __init__(self, image, r):
        self.image = image
        self.r = r

        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.resultx = 0
        self.resulty = 0

    def onclick(self, event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))
        x = math.ceil(event.xdata)
        y = math.ceil(event.ydata)

        #plt.scatter(x, y, s=self.r, c='blue', marker='s', alpha=1)
        #plt.scatter(x - self.r / 2, y - self.r / 2, s=self.r, c='green', marker='s', alpha=1)

        rect = plt.Rectangle((x - self.r / 2, y - self.r / 2), width=self.r, height=self.r, fc='red', alpha=0.4)
        plt.gca().add_patch(rect)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        self.resultx = math.ceil(event.xdata)
        self.resulty = math.ceil(event.ydata)

        time.sleep(2)
        plt.close()

    def create_device(self):
        plt.imshow(self.image, cmap='gray')
        plt.show()
        return self.resultx, self.resulty


def select_coord_on_img(img, R):
    devcr = CoordSelector(img, R)
    x, y = devcr.create_device()
    return x, y



if __name__ == '__main__':
    pass