from default_prediction_generator import DefaultPredictionsGenerator
from w_wrapper import W_wrapper
from common_utils import *
from hand_creator_of_exemplar import HandGeneratedTraj, restore_saved_traj
import matplotlib.pyplot as plt

def handli_fill_facts(pic):
    # hand_creator_of_ex = HandGeneratedTraj(pic)
    # hand_creator_of_ex.fill_traj_with_radiuses()
    hand_creator_of_ex = restore_saved_traj()

    prediction_gen = DefaultPredictionsGenerator(pic)

    for i in range(len(hand_creator_of_ex.radiuses)):
        radius = hand_creator_of_ex.radiuses[i]
        point = hand_creator_of_ex.points[i]

        point_cloud = pic.get_point_cloud(point, radius)
        mean = pic.get_mean_color_in_point_cloud(point_cloud)
        prediction_gen.add_fact(point_cloud, mean)

    return prediction_gen

def handli_measure_some_facts(pic):
    hand_creator_of_ex = HandGeneratedTraj(pic)
    hand_creator_of_ex.fill_traj_with_radiuses()
    centers, radiuses = hand_creator_of_ex.points, hand_creator_of_ex.radiuses
    means =[pic.get_mean_color_in_point_cloud(pic.get_point_cloud(centers[i], radiuses[i])) for i in range(len(centers))]
    return centers, means, radiuses

def test_disentangled():
    logger = HtmlLogger("HAND_TEST_w_dis")
    pic = Pic()

    #заполним сначала контекст, потому что ценности новых фактов меряются относительно уже имеющихся известных фактов
    default_preds_generator = handli_fill_facts(pic)
    logger.add_fig(default_preds_generator.draw())

    # накликиваем факты, полезность которых будем мерить
    centers, means, radiuses = handli_measure_some_facts(pic)
    N = len(centers)

    w_wrapper = W_wrapper(pic)
    for i in range(N):
        new_pred = means[i]
        pred_radius = radiuses[i]
        point = centers[i]
        w = w_wrapper.eval_disentangled_w(new_pred, point, pred_radius, default_preds_generator)
        print(w)
        fig, ax = plt.subplots()
        default_preds_generator.draw_to_ax(ax)
        points_cloud = pic.get_point_cloud(point, pred_radius)
        for point_ in points_cloud:
            ax.scatter(point_.x, point_.y, color='r')
        logger.add_text("w = " + str(w) + " :")
        logger.add_fig(fig)

if __name__ == '__main__':
    test_disentangled()