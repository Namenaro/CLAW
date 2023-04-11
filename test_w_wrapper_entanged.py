from default_prediction_generator import DefaultPredictionsGenerator
from w_wrapper import W_wrapper
from common_utils import *
from hand_creator_of_exemplar import HandGeneratedTraj, restore_saved_traj
import matplotlib.pyplot as plt

def handli_fill_facts(pic):
    hand_creator_of_ex = HandGeneratedTraj(pic)
    # hand_creator_of_ex.fill_traj_with_radiuses()
    #hand_creator_of_ex = restore_saved_traj()

    prediction_gen = DefaultPredictionsGenerator(pic)

    for i in range(len(hand_creator_of_ex.radiuses)):
        radius = hand_creator_of_ex.radiuses[i]
        point = hand_creator_of_ex.points[i]

        point_cloud = pic.get_point_cloud(point, radius)
        mean = pic.get_mean_color_in_point_cloud(point_cloud)
        prediction_gen.add_fact(point_cloud, mean)

    return prediction_gen


def handli_create_prediction(pic):
    print(" Ткнуть одну точку и ей ввести радиус: чисто чтоб задать предсказание вида (радиус, среднее):")
    # факт для которого мы будем мерить запутанную ценность (нужен один клик)
    hand_creator_of_ex = HandGeneratedTraj(pic)
    hand_creator_of_ex.fill_traj_with_radiuses()
    centers, radiuses = hand_creator_of_ex.points, hand_creator_of_ex.radiuses
    center = centers[0]
    radius = radiuses[0]
    mean = pic.get_mean_color_in_point_cloud(pic.get_point_cloud(center, radius))
    return mean, radius

def hendli_select_n_plus_one_ponints(pic):
    print(" Тыкаем без радиусов. Первую точку расчитываем,"
          " как точку, где должно выполниться предсказание, "
          "а остальные - как точки, в которых будет считаться запутанное w" )
    hand_creator_of_ex = HandGeneratedTraj(pic)
    hand_creator_of_ex.fill_traj_no_radiuses()
    points = hand_creator_of_ex.points
    return points

def test_entangled():
    logger = HtmlLogger("HAND_TEST_w_ent")
    pic = Pic()

    #заполним сначала контекст, потому что ценности новых фактов меряются относительно уже имеющихся известных фактов
    default_preds_generator = handli_fill_facts(pic)
    logger.add_fig(default_preds_generator.draw())

    # теперь создаем предсказание: радиус и среднее (ткнем один раз):
    mean, radius = handli_create_prediction(pic)
    print("mean="+ str(mean)+ ", rad="+ str(radius))

    # теперь будм мерять запутанность сенсора с действием. Для этого нужна точка, где "предсказано",
    # и произвольные точки, где им хотим отностельно ее померить w_ebntangled
    points = hendli_select_n_plus_one_ponints(pic)

    center_point = points[0]
    w_wrapper = W_wrapper(pic)

    for point in points:
        error_radius = (point - center_point).norm()+1
        w = w_wrapper.eval_entangled_w(error_radius=error_radius,
                                       new_pred=mean,
                                       point=point,
                                       pred_radius=radius,
                                       default_preds_generator=default_preds_generator)
        print(w)
        fig, ax = plt.subplots()
        default_preds_generator.draw_to_ax(ax)
        points_cloud = pic.get_point_cloud(point, radius)
        for point_ in points_cloud:
            ax.scatter(point_.x, point_.y, color='g')
        logger.add_text("w_ent = " + str(w) + " :")
        logger.add_fig(fig)

if __name__ == '__main__':
    test_entangled()
