from default_prediction_generator import DefaultPredictionsGenerator
from common_utils import *
from hand_creator_of_exemplar import HandGeneratedTraj, restore_saved_traj


if __name__ == '__main__':
    logger = HtmlLogger("HAND_TEST1")
    pic = Pic()
    prediction_gen = DefaultPredictionsGenerator(pic)


    #hand_creator_of_ex = HandGeneratedTraj(pic)
    #hand_creator_of_ex.fill_traj_with_radiuses()
    hand_creator_of_ex=restore_saved_traj()

    logger.add_text(str(len(prediction_gen.regions_dict)) + " regions:")
    fig = prediction_gen.draw()
    logger.add_fig(fig)

    for i in range(len(hand_creator_of_ex.radiuses)):
        radius = hand_creator_of_ex.radiuses[i]
        point = hand_creator_of_ex.points[i]

        point_cloud = pic.get_point_cloud(point, radius)
        mean = pic.get_mean_color_in_point_cloud(point_cloud)
        prediction_gen.add_fact(point_cloud, mean)
        fig = prediction_gen.draw()
        logger.add_text(str(len(prediction_gen.regions_dict)) + " regions:")
        logger.add_fig(fig)

