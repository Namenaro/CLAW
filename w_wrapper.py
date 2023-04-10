from w_evaluator import W_Evaluator
from default_prediction_generator import DefaultPredictionsGenerator
from common_utils import Pic, Point


class W_wrapper:
    def __init__(self, pic):
        self.pic = pic
        self.evaluator = W_Evaluator(self.pic)

    def eval_disentangled_w(self, new_pred, point, pred_radius, default_preds_generator):
        points_cloud = self.pic.get_point_cloud(center_point=point, radius=pred_radius)
        old_pred = default_preds_generator.get_mean_in_region(points_list=points_cloud)
        real_values_cloud = self.pic.get_vals_of_point_cloud(points_cloud)
        return self.evaluator.get_w_for_point_cloud(old_pred=old_pred, new_pred=new_pred, real_values_cloud=real_values_cloud)

    def get_theoretical_max_w_disenatgled(self, pred_radius):
        return self.pic.get_num_points_in_vicitiny(pred_radius)

    def eval_entangled_w(self, error_radius, new_pred, point, pred_radius, default_preds_generator):
        points_cloud = self.pic.get_point_cloud(center_point=point, radius=pred_radius)
        old_pred = default_preds_generator.get_mean_in_region(points_list=points_cloud)
        real_values_cloud = self.pic.get_vals_of_point_cloud(points_cloud)
        real_w = self.evaluator.get_w_for_point_cloud(old_pred=old_pred, new_pred=new_pred, real_values_cloud=real_values_cloud)

        sample_maxes_w = self.evaluator.get_maxes_w_distr( search_radius=error_radius, old_pred=old_pred, new_pred=new_pred, pred_radius=pred_radius)
        w = self.evaluator.entangle_real_w(sample_maxes_w=sample_maxes_w, real_w=real_w,
                                       THEORETICAL_MAX_w=self.get_theoretical_max_w_disenatgled(pred_radius=pred_radius))
        return w
