from common_utils import Pic, Distr, HtmlLogger
from default_prediction_generator import DefaultPredictionsGenerator
from common_utils import Pic, Point

import numpy as np

import matplotlib.pyplot as plt
class W_wrapper:
    def __init__(self, pic):
        self.pic = pic


    def eval_disentangled_w(self, new_pred, point, pred_radius, default_preds_generator):
        points_cloud = self.pic.get_point_cloud(center_point=point, radius=pred_radius)
        old_pred = default_preds_generator.get_mean_in_region(points_list=points_cloud)
        real_values_cloud = self.pic.get_vals_of_point_cloud(points_cloud)
        return self.get_w_for_point_cloud(old_pred=old_pred, new_pred=new_pred, real_values_cloud=real_values_cloud)

    def get_theoretical_max_w_disenatgled(self, pred_radius):
        return self.pic.get_num_points_in_vicitiny(pred_radius)

    def eval_entangled_w(self, error_radius, new_pred, point, pred_radius, default_preds_generator):
        points_cloud = self.pic.get_point_cloud(center_point=point, radius=pred_radius)
        old_pred = default_preds_generator.get_mean_in_region(points_list=points_cloud)
        real_values_cloud = self.pic.get_vals_of_point_cloud(points_cloud)
        real_w = self.get_w_for_point_cloud(old_pred=old_pred, new_pred=new_pred, real_values_cloud=real_values_cloud)

        sample_maxes_w = self.get_maxes_w_distr( search_radius=error_radius, old_pred=old_pred, new_pred=new_pred, pred_radius=pred_radius)
        w = self.entangle_real_w(sample_maxes_w=sample_maxes_w, real_w=real_w,
                                       THEORETICAL_MAX_w=self.get_theoretical_max_w_disenatgled(pred_radius=pred_radius))
        #plt.hist(sample_maxes_w)
        #plt.show()
        return w

    def get_w_for_1px(self, old_pred, new_pred, real_value):
        distr = self.pic.distr
        curr_profit = 1 - distr.get_p_of_event(real_value, old_pred)
        new_profit = 1 - distr.get_p_of_event(real_value, new_pred)
        w = new_profit - curr_profit
        return w  # [-1,1]

    def get_w_for_point_cloud(self, old_pred, new_pred, real_values_cloud):
        w_in_cloud = 0
        for real_val in real_values_cloud:
            w_in_point = self.get_w_for_1px(old_pred=old_pred, new_pred=new_pred, real_value=real_val)
            w_in_cloud += w_in_point
        return w_in_cloud  # [- len(cloud), + len(cloud)]


    def get_maxes_w_distr(self, search_radius, old_pred, new_pred, pred_radius):
        SAMPLE_SIZE = 120
        sample_maxes = []
        for i in range(SAMPLE_SIZE):
            sample1px = self.pic.distr.get_sample(sample_size=self.pic.get_num_points_in_vicitiny(search_radius+pred_radius))
            # обходим все пикслели и считаем однопиксельное w
            w_1ps = []
            for real_val in sample1px:
                w_1p = self.get_w_for_1px(old_pred=old_pred, new_pred=new_pred, real_value=real_val)
                w_1ps.append(w_1p)

            # выбираем из них топ Н лучших, где Н - размер обалсти предсказания
            size_of_prediction = self.pic.get_num_points_in_vicitiny(pred_radius)
            best_w1s = (sorted(w_1ps, reverse=True))[0:size_of_prediction]
            best_w1s_positive = [item for item in best_w1s if item >= 0]
            # из сумму выигрыша добавляем в sample_maxes
            sample_maxes.append(sum(best_w1s))
        return sample_maxes # каждое число в семпле [- len(cloud), + len(cloud)]

    def entangle_real_w(self, sample_maxes_w, real_w, THEORETICAL_MAX_w):
        distr_maxes = Distr(max=THEORETICAL_MAX_w, min=-THEORETICAL_MAX_w, sample=sample_maxes_w)
        w_max_prediction = distr_maxes.get_mean()
        p = distr_maxes.get_p_of_event(val_1=real_w, val_2=w_max_prediction)
        if real_w > w_max_prediction:
            return p
        return -p  # [-1,1]


# ТЕСТЫ ======
def test_max_w_sampler():
    logger = HtmlLogger("HAND_TEST_w_maxes")
    pic = Pic()
    old_pred = pic.get_mean()
    new_pred = 250
    pred_radius = 1

    wrapper = W_wrapper(pic)
    max_w_wal = wrapper.get_theoretical_max_w_disenatgled(pred_radius)
    print("max_w=" + str(max_w_wal))
    radiuses = list(range(10, 18, 2))
    expected_w_maxes = []
    for search_radius in radiuses:
        max_sample = wrapper.get_maxes_w_distr(search_radius, old_pred, new_pred, pred_radius)
        expected_w_maxes.append(np.mean(max_sample))
        fig, ax = plt.subplots()
        ax.hist(max_sample, range=[-max_w_wal, max_w_wal], bins=50)
        logger.add_text("search_radius =  " + str(search_radius))
        logger.add_fig(fig)

    plt.plot(radiuses, expected_w_maxes)
    plt.show()

def test_w_ipx():
    pic = Pic()
    old_pred = pic.get_mean()
    new_pred = 5
    real_value = 10

    distr = pic.distr
    plt.hist(distr.sample, bins=100)
    plt.show()
    curr_profit = 1 - distr.get_p_of_event(real_value, old_pred)
    new_profit = 1 - distr.get_p_of_event(real_value, new_pred)
    w = new_profit - curr_profit
    print(w)

if __name__ == '__main__':
    #test_max_w_sampler()
    test_w_ipx()
