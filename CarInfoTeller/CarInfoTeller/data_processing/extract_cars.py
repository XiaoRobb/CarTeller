"""
    - Script to extract cars from image
"""
from scipy import io as mat_io
from skimage import io as img_io
import argparse
import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(0)


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Extract Cars')

    args.add_argument('-m', '--meta', default='datasets/cars_metas/cars_test_annos', type=str,
                      help='cars train meta (default: test)')
    args.add_argument('-i', '--input', default='datasets/testing/original/', type=str,
                      help='input folder')
    args.add_argument('-o', '--output', default='datasets/testing/extracted/', type=str,
                      help='output folder')
    parsed = args.parse_args()
    metas = parsed.meta
    original_folder = parsed.input
    extracted_folder = parsed.output

    labels_meta = mat_io.loadmat(metas)

    for img_ in labels_meta['annotations'][0]:
        x_min = img_[0][0][0]
        y_min = img_[1][0][0]

        x_max = img_[2][0][0]
        y_max = img_[3][0][0]

        if len(img_) == 6:
            img_name = img_[5][0]
        elif len(img_) == 5:
            img_name = img_[4][0]
        try:
            img_in = img_io.imread(original_folder + img_name)
        except Exception:
            print("Error while reading!")
        else:
            # print(img_in.shape)
            cars_extracted = img_in[y_min:y_max, x_min:x_max]
            _logger.info(x_min, y_min, x_max, y_max, cars_extracted.shape, img_in.shape, img_name)

            img_io.imsave(extracted_folder + img_name, cars_extracted)

