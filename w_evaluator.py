from common_utils import Pic, Distr

class W_Evaluator:
    def __init__(self, pic):
        self.pic = pic

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

    def get_w_in_random_cloud(self, old_pred, new_pred, pred_radius):
        sample1px = self.pic.distr.sample(sample_size=self.pic.get_num_points_in_vicitiny(pred_radius))
        w_in_random_cloud = self.get_w_for_point_cloud(old_pred=old_pred, new_pred=new_pred, real_values_cloud=sample1px)
        return w_in_random_cloud  # [- len(cloud), + len(cloud)]

    def get_maxes_w_distr(self, search_radius, old_pred, new_pred, pred_radius):
        SAMPLE_SIZE = 40
        sample_maxes = []
        for i in range(SAMPLE_SIZE):
            sample_sarch_traj = []
            for j in range(self.pic.get_num_points_in_vicitiny(search_radius)):
                sample_sarch_traj.append(self.get_w_in_random_cloud(old_pred=old_pred, new_pred=new_pred, pred_radius=pred_radius))
                sample_maxes.append(max(sample_sarch_traj))
        return sample_maxes # каждое числов семпле [- len(cloud), + len(cloud)]

    def entangle_real_w(self, sample_maxes_w, real_w, THEORETICAL_MAX_w):
        distr_maxes = Distr(max=THEORETICAL_MAX_w, min=-THEORETICAL_MAX_w, sample=sample_maxes_w)
        w_max_prediction = distr_maxes.get_mean()
        p = distr_maxes.get_p_of_event(val_1=real_w, val_2=w_max_prediction)
        if real_w > w_max_prediction:
            return p
        return -p  # [-1,1]

