from common_utils import IdsGenerator

from copy import deepcopy

class DefaultPredictionsGenerator:
    def __init__(self, pic_point_list, mean_in_pic):
        self.pic_point_list = pic_point_list
        self.regions_dict = {}
        self.ids_generation = IdsGenerator()
        initial_reg_id = self.ids_generation.generate_id()
        self.regions_dict[initial_reg_id]=Region(pic_point_list, mean_in_pic)


    def get_mean_in_region(self, points_list):
        sum = 0
        for point in points_list:
            sum += self._get_mean_for_point(point)
        mean = sum/len(points_list)
        return mean

    def add_fact(self, points_list, real_mean):
        current_reg_ids = deepcopy(self.regions_dict.keys())
        for reg_id in current_reg_ids:
            region_to_divide = self.regions_dict[reg_id]
            intersecton, outer = self._get_AandB_AnoB(region_to_divide.points, point_cloudB=points_list)
            if len(intersecton) == 0:
                continue
            self._handle_intersection(self, intersecton, outer,
                                      reg_id_to_divide=reg_id,
                                      reg_mean=region_to_divide.mean,
                                      fact_mean=real_mean)

    def _handle_intersection(self, intersecton, outer, reg_id_to_divide, reg_mean, fact_mean):
        # создаем регион-пересечение:
        mean_in_intersection = (reg_mean + fact_mean)/2
        intersecton_region = Region(points=intersecton, mean=mean_in_intersection)
        reg_id_intersection = self.ids_generation.generate_id()
        self.regions_dict[reg_id_intersection] = intersecton_region

        # создаем регион вне пересечения, но внутри разделяемого региона:
        mass_of_intersection = len(intersecton) + mean_in_intersection
        mass_of_region_to_divide = self.regions_dict[reg_id_to_divide].get_mass()
        mass_of_outer = mass_of_region_to_divide - mass_of_intersection
        mean_of_outer = mass_of_outer/len(outer)
        outer_region = Region(points=outer, mean=mean_of_outer)
        reg_id_outer = self.ids_generation.generate_id()
        self.regions_dict[reg_id_outer] = outer_region

        # удаляем разделенный на два теперь регион:
        del self.regions_dict[reg_id_to_divide]

    def _get_AandB_AnoB(self, point_cloudA_to_devide, point_cloudB):
        intersecton = []
        outer = []
        for point_a in point_cloudA_to_devide:
            if point_a in point_cloudB:
                intersecton.append(deepcopy(point_a))
            else:
                outer.append(deepcopy(point_a))
        return intersecton, outer

    def _get_mean_for_point(self, point):
        for reg_id, region in self.regions_dict.items():
            if region.has_point(point):
                return region.mean

class Region:
    def __init__(self, points, mean):
        self.points = points
        self.mean = mean

    def has_point(self, point):
        if point in self.points:
            return True
        return False

    def get_mass(self):
        return len(self.points)+self.mean
