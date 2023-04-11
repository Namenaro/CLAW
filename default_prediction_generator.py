from common_utils import IdsGenerator, Pic, Point

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
import numpy as np
from copy import deepcopy


class DefaultPredictionsGenerator:
    def __init__(self, pic):
        self.pic = pic
        self.regions_dict = {}
        self.ids_generation = IdsGenerator()
        initial_reg_id = self.ids_generation.generate_id()
        self.regions_dict[initial_reg_id] = Region(pic.get_coords_list(), pic.get_mean())

    def get_mean_in_region(self, points_list):
        sum = 0
        for point in points_list:
            sum += self._get_mean_for_point(point)
        mean = sum / len(points_list)
        return mean


    def draw(self):
        numpy_pic = np.zeros(shape=self.pic.img.shape)
        new_pic = Pic(numpy_pic)
        fig, ax = plt.subplots()
        for _, region in self.regions_dict.items():
            region.draw_to_pic(new_pic)
        new_pic.draw_to_ax(ax)

        # фон
        cm = plt.get_cmap('Greens')
        ax.imshow(self.pic.img, cmap=cm, alpha=0.1)
        return fig

    def draw_to_ax(self, ax):
        numpy_pic = np.zeros(shape=self.pic.img.shape)
        new_pic = Pic(numpy_pic)
        for _, region in self.regions_dict.items():
            region.draw_to_pic(new_pic)
        new_pic.draw_to_ax(ax)
        # фон
        cm = plt.get_cmap('Greens')
        ax.imshow(self.pic.img, cmap=cm, alpha=0.07)

    def add_fact(self, fact_points, fact_mean):
        region_ids, inners_points, outers_points = self._find_all_intersections(fact_points)
        means_of_intersected_regions = [self.regions_dict[reg_id].mean for reg_id in region_ids]
        sizes_of_intersections = [len(points_intersection) for points_intersection in inners_points]
        sizes_of_outers = [len(points_outer) for points_outer in outers_points]
        fact_mass = fact_mean*len(fact_points)

        unnormed_ratios = [sizes_of_intersections[i]/(len(fact_points)) for i in range(len(region_ids))]
        divider = sum(unnormed_ratios)
        ratios = [unnormed_ratios[i]/divider for i in range(len(unnormed_ratios))]
        koeff = self._kalc_koeff(fact_mass, sizes_of_intersections=sizes_of_intersections,
                                 means_of_intersected_regions=means_of_intersected_regions,
                                 ratios=ratios)
        means_for_all_intersections = self._kalc_means_for_all_intersections(koeff, means_of_intersected_regions, ratios=ratios)

        means_for_all_outers = self._kals_means_for_all_outer_regions(means_for_all_intersections=means_for_all_intersections,
                                                                      outers_lens=sizes_of_outers,
                                                                      inners_lens=sizes_of_intersections,
                                                                      means_of_intersected_regions=means_of_intersected_regions)
        for i in range(len(region_ids)):
            self._delete_region(region_ids[i])

            mean_of_intersection = means_for_all_intersections[i]
            points_of_intersection = inners_points[i]
            self._add_new_region(mean=mean_of_intersection, points=points_of_intersection)

            mean_of_outer = means_for_all_outers[i]
            points_of_outer = outers_points[i]
            self._add_new_region(mean=mean_of_outer, points=points_of_outer)

    def _find_all_intersections(self, fact_points):
        region_ids = []
        inners_points = []
        outers_points = []

        for region_id, region in self.regions_dict.items():
            intersecton, outer = self._get_AandB_AnoB(point_cloudA_to_divide=region.points,
                                                      point_cloudB=fact_points)
            if len(intersecton) == 0:
                continue
            region_ids.append(region_id)
            inners_points.append(intersecton)
            outers_points.append(outer)
        return region_ids, inners_points, outers_points

    def _kalc_koeff(self, fact_mass, sizes_of_intersections, means_of_intersected_regions, ratios):
        num_intersections = len(sizes_of_intersections)
        unnormed_masses_of_intersections = [sizes_of_intersections[i]*means_of_intersected_regions[i]*ratios[i]
                                            for i in range(num_intersections)]
        if fact_mass == 0:
            return None
        koeff = sum(unnormed_masses_of_intersections)/fact_mass

        return koeff

    def _kalc_means_for_all_intersections(self, koeff, means_of_intersected_regions, ratios):
        N = len(means_of_intersected_regions)
        if koeff is None:
            return [0]*N
        means_for_all_intersections = [means_of_intersected_regions[i]* ratios[i]/koeff for i in range(N)]
        return means_for_all_intersections

    def _kals_means_for_all_outer_regions(self, means_for_all_intersections, outers_lens, inners_lens,
                                          means_of_intersected_regions):
        N = len(outers_lens)
        masses_of_intersected_regions = [means_of_intersected_regions[i]*(outers_lens[i]+inners_lens[i]) for i in range(N)]
        masses_of_intersections = [means_for_all_intersections[i]*inners_lens[i] for i in range(N)]
        means_for_all_outer_regions = [(masses_of_intersected_regions[i]-masses_of_intersections[i])/outers_lens[i] for i in range(N)]
        return means_for_all_outer_regions

    def _add_new_region(self, mean, points):
        reg_id = self.ids_generation.generate_id()
        new_region = Region(points=points, mean=mean)
        self.regions_dict[reg_id] = new_region

    def _delete_region(self, reg_id):
        del self.regions_dict[reg_id]


    def _get_AandB_AnoB(self, point_cloudA_to_divide, point_cloudB):
        intersecton = []
        outer = []
        for point_a in point_cloudA_to_divide:
            if point_a in point_cloudB:
                intersecton.append(deepcopy(point_a))
            else:
                outer.append(deepcopy(point_a))
        return intersecton, outer

    def _get_mean_for_point(self, point):
        for reg_id, region in self.regions_dict.items():
            if region.has_point(point):
                return region.mean

    def print_means(self):
        str_means = ""
        for reg_id, region in self.regions_dict.items():
            str_means += str(reg_id) + ": " + str(region.mean) + ", "
        return str_means

class Region:
    def __init__(self, points, mean):
        self.points = points
        self.mean = mean

    def has_point(self, point):
        if point in self.points:
            return True
        return False

    def get_mass(self):
        return len(self.points) + self.mean

    def draw_to_pic(self, pic):
        for point in self.points:
            pic.set_point_color(point, color=self.mean)


if __name__ == '__main__':
    pic = Pic()
    prediction_gen = DefaultPredictionsGenerator(pic)
    prediction_gen.draw()
    plt.show()

    point = pic.get_center_point()
    radius = 4
    points_cloud = pic.get_point_cloud(point, radius=radius)
    mean_in_cloud = pic.get_mean_color_in_point_cloud(points_cloud)
    prediction_gen.add_fact(points_cloud, mean_in_cloud)
    prediction_gen.draw()
    plt.show()

    point = point + Point(0, 3)
    radius = 8
    points_cloud = pic.get_point_cloud(point, radius=radius)
    mean_in_cloud = pic.get_mean_color_in_point_cloud(points_cloud)
    prediction_gen.add_fact(points_cloud, mean_in_cloud)
    prediction_gen.draw()
    plt.show()
