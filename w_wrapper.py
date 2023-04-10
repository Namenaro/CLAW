from w_evaluator import W_Evaluator
from default_prediction_generator import DefaultPredictionsGenerator
from common_utils import Pic, Point

def eval_disentangled_profit(pic, new_pred, point, pred_radius, default_preds_generator):
    evaluator = W_Evaluator(pic)
    points_cloud = pic.get_point_cloud(center_point=point, radius=pred_radius)
    old_pred = default_preds_generator.get_mean_in_region(points_list=points_cloud)
    real_values_cloud = pic.get_vals_of_point_cloud(points_cloud)
    return evaluator.get_w_for_point_cloud(old_pred=old_pred, new_pred=new_pred, real_values_cloud=real_values_cloud)

def eval_entangled_profit(error_radius, pic, new_pred, point, pred_radius, default_preds_generator):
    return w