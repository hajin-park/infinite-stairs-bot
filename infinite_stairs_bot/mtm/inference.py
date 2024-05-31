from MTM import matchTemplates, drawBoxesOnRGB
import cv2


class MultiTemplateMatch:
    def __init__(self):
        pass

    def predict(self, listTemplates, image):
        hits = matchTemplates(
            listTemplates,
            image,
            method=cv2.TM_CCOEFF_NORMED,
            N_object=float("inf"),
            score_threshold=0.7,
            maxOverlap=0,
            searchBox=None,
        )

        return hits

    def annotate_img(self, img, hits):
        annotated_image = drawBoxesOnRGB(
            img,
            hits,
            boxThickness=2,
            boxColor=(255, 0, 255),
            showLabel=True,
            labelColor=(0, 0, 0),
            labelScale=0.5,
        )

        return annotated_image
