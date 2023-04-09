from common_utils import Point

import numpy as np
import random
import torchvision.datasets as datasets
import os
import matplotlib.pyplot as plt
from math import ceil

class Pic:
    def __init__(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(dir_path, './MNIST')
        self.dataset = datasets.MNIST(root=path, train=True, download=True, transform=None)
        class_of_pisc = 3
        for element in self.dataset:
            if element[1] == class_of_pisc:
                self.img = np.array(element[0])
                break

    def show(self):
        plt.imshow(self.img, cmap='gray', interpolation='none')
        plt.show()

    def get_coords_list(self):
        points_list = []
        for x in range(0, self.img.shape[1]):
            for y in range(0, self.img.shape[0]):
                points_list.append(Point(x=x, y=y))
        return points_list

    def get_bright_in_point(self, point):
        return self.img[point.y][point.x]

    def get_center_point(self):
        Y=self.img.shape[0]
        X=self.img.shape[1]
        center_x = ceil(X/2)
        center_y = ceil(Y / 2)
        return Point(x=center_x, y=center_y)

    def get_bio1_sample(self, sample_size=80):
        full_sample = self.img.ravel()
        S_1 = [random.choice(full_sample) for _ in range(sample_size)]
        return S_1


    def draw_to_ax(self, ax):
        ax.imshow(self.img, cmap='gray', interpolation='none')


if __name__ == '__main__':
    pic = Pic()
    #pic.show()

    fig, ax = plt.subplots()
    pic.draw_to_ax(ax)
    center_point = pic.get_center_point()
    ax.scatter(center_point.x, center_point.y, s=200, c='r')
    plt.show()
    plt.close(fig)

    sample = pic.get_bio1_sample(177)
    plt.hist(sample)
    plt.show()


