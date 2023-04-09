from pic_getter import Pic
from common_utils import Point

import matplotlib.pyplot as plt
import math
import time

class HandGeneratedTraj:
    def __init__(self, pic):
        self.pic = pic
        self.points = []
        self.radiuses = []

    def fill_traj_with_radiuses(self):
        self.points, self.radiuses = select_coord_on_img(self.pic.img, need_radiuses=True)

    def fill_traj_no_radiuses(self):
        self.points, self.radiuses = select_coord_on_img(self.pic.img, need_radiuses=False)

    def fill_traj_const_radius(self, radius):
        self.points, self.radiuses = select_coord_on_img(self.pic.img, need_radiuses=True)
        self.radiuses = [radius] * len(self.points)

    def draw(self):
        pass



# правая кропка закрыть
class CoordSelector:
    def __init__(self, image, need_radiuses=False):
        self.image = image
        self.need_radiuses = need_radiuses
        self.r = 4

        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.result_points = []
        self.result_radiuses = []

    def onclick(self, event):
        #print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
        #      ('double' if event.dblclick else 'single', event.button,
        #       event.x, event.y, event.xdata, event.ydata))
        if event.button != 1:
            #time.sleep(2)
            plt.close()
            return
        x = math.ceil(event.xdata)
        y = math.ceil(event.ydata)
        point = Point(x=x, y=y)
        self.result_points.append(point)
        if self.need_radiuses:
            radius = int(input("Enter radius: "))
            self.result_radiuses.append(radius)
        else:
            radius = self.r

        rect = plt.Rectangle((x - radius / 2, y - radius / 2), width=radius, height=radius, fc='red', alpha=0.4)
        plt.gca().add_patch(rect)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        self.resultx = math.ceil(event.xdata)
        self.resulty = math.ceil(event.ydata)

    def create_device(self):
        plt.imshow(self.image, cmap='gray')
        plt.show()
        return self.result_points, self.result_radiuses


def select_coord_on_img(img, need_radiuses):
    devcr = CoordSelector(img, need_radiuses)
    x, y = devcr.create_device()
    return x, y



if __name__ == '__main__':
    pic = Pic()
    hand_creator_of_ex = HandGeneratedTraj(pic)
    hand_creator_of_ex.fill_traj_with_radiuses()
    print(str(hand_creator_of_ex.radiuses))

