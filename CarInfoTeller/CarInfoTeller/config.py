import torch
from scipy import io as mat_io

car_mat_file = "./data_processing/datasets/cars_metas/cars_meta"
labels_meta = mat_io.loadmat(car_mat_file)
class_names = [name[0] for name in labels_meta['class_names'][0]]

use_gpu_all = torch.cuda.is_available()


class ConfigTrain:
    best_acc1 = 0
    model_name = 'efficientnet-b4'
    batch_size = 2
    epochs = 90
    start_epoch = 0
    num_wokers = 4
    lr = 0.1
    weight_decay = 1e-4
    momentum = 0.9
    use_gpu = use_gpu_all
    print_freq = 100
    resume_file = "./checkpoints/model_best.pth.tar"
    data_dir = './data_processing/datasets/'
    num_classes = len(class_names)


opt_train = ConfigTrain()
