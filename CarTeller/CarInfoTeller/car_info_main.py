import argparse
import torch
import CarInfoTeller.model.model as module_arch
from parse_config import ConfigParser
from torchvision import transforms
from skimage import io
import scipy.io as mat_io
import cv2
import os
import sys
import gc

def get_labels():
    car_mat_file = "./cars_meta"
    labels_meta = mat_io.loadmat(car_mat_file)
    labels_map = [name[0] for name in labels_meta['class_names'][0]]
    names = [line[:-1] for line in open('./cars_translated.txt', 'r', encoding='UTF-8')]
    return labels_map, names


def predict(config, resume, image):
    """
    汽车车型识别
    :param config: ****
    :param resume: ****
    :param image: cv2格式
    :return:车型信息， 对应概率，一共返回有5个可能车型
    """

    # build model architecture
    model = config.initialize('arch', module_arch)
    print(resume)
    checkpoint = torch.load(resume,map_location='cpu')
    state_dict = checkpoint['state_dict']
    if config['n_gpu'] > 1:
        model = torch.nn.DataParallel(model)
    model.load_state_dict(state_dict)

    # prepare model for testing
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    model.eval()

    # 图片处理
    image = cv2.resize(image, (299, 299), interpolation=cv2.INTER_CUBIC)
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        image = image.to(device)
        output = model(image)
        preds = torch.topk(output, k=5)[1].squeeze(0).tolist()
        labels_map, names = get_labels()
        infos = [labels_map[idx] + "(" + names[idx] + ")" for idx in preds]
        pros = [torch.softmax(output, dim=1)[0, idx].item() for idx in preds]
        del model
        gc.collect()
        return infos, pros


def car_info_tell(img):
    """
    汽车车型识别
    :param img: cv2格式
    :return:
    """
    parser = argparse.ArgumentParser(description='Cars Test')

    parser.add_argument( '--phase', default='test', type=str,
                        help='phase (default: None)')
    parser.add_argument( '--config', default='./test_config.json', type=str,
                        help='config file path (default: None)')
    parser.add_argument( '--model', default='./model_best.pth',
                        type=str,
                        help='path to model (default: None)')
    parser.add_argument('--device', default=None, type=str,
                        help='indices of GPUs to enable (default: all)')
    
    print(sys.argv[1:])
    args,unknown = parser.parse_known_args(["test","./test_config.json","./model_best.path"])
    config = ConfigParser(parser)
    infos, pros = predict(config, args.model, img)
    return infos, pros   # 车型信息， 对应概率，一共返回有5个可能车型


if __name__ == '__main__':

    image = io.imread("./test.jpg")
    infos, pros = car_info_tell(image)
    for item in zip(infos, pros):
        print(item)
