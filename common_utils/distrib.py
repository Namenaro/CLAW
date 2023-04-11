import numpy as np
import matplotlib.pyplot as plt
from random import choices


class Distr:
    def __init__(self, max, min, sample=None):
        self.max = max
        self.min = min
        self.uniform = False

        if sample is None:
            self.uniform = True

        self.sample = sample

    def get_p_of_event(self, val_1, val_2):

        if val_1 < val_2:
            left = val_1
            right = val_2

        elif val_1 > val_2:
            left = val_2
            right = val_1

        elif val_1 == val_2:
            return 0

        if self.uniform:
            return (right - left) / (self.max - self.min)

        counts = [el for el in self.sample if left <= el <= right]

        return len(counts) / len(self.sample)

    def draw(self):
        if not self.uniform:
            fig, ax = plt.subplots()
            plt.hist(self.sample, density=True, edgecolor="black")
            plt.show()
        else:

            fig, ax = plt.subplots()
            tmp_sample = np.random.uniform(self.min, self.max, 200)
            plt.hist(tmp_sample, density=True, edgecolor="black")
            plt.show()

        return fig

    def get_mean(self):
        if not self.uniform:
            return np.mean(self.sample)
        else:
            return (self.max + self.min) / 2


    def get_sample(self, sample_size):
        return choices(self.sample, k=sample_size)
