"""
Evaluate on ImageNet. Note that at the moment, training is not implemented (I am working on it).
that being said, evaluation is working.
"""

import argparse
import os
import random
import shutil
import time
import warnings
from PIL import Image

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
from efficientnet_pytorch import EfficientNet
from scipy import io as mat_io


car_mat_file = "./data_processing/datasets/cars_metas/cars_meta"
labels_meta = mat_io.loadmat(car_mat_file)
labels_map = [name[0] for name in labels_meta['class_names'][0]]
use_gpu = torch.cuda.is_available()
print(use_gpu)
resume_file = "./checkpoints/model_best.pth.tar"
num_classes = len(labels_map)

model_name = 'efficientnet-b4'
batch_size = 2
num_wokers = 4
lr = 0.1
weight_decay = 1e-4
momentum = 0.9


def tell(img):

    # 创建网络模型
    model = EfficientNet.from_pretrained(model_name, num_classes=num_classes)
    if use_gpu:
        model.cuda()

    # 损失函数和优化器
    criterion = nn.CrossEntropyLoss().cuda()
    optimizer = torch.optim.SGD(model.parameters(), lr,
                                momentum=momentum,
                                weight_decay=weight_decay)

    # 是加载已有的模型
    print("=> loading checkpoint '{}'".format(resume_file))
    checkpoint = torch.load(resume_file)
    model.load_state_dict(checkpoint['state_dict'])
    print("=> loaded checkpoint '{}' (epoch {})".format(resume_file, checkpoint['epoch']))

    cudnn.benchmark = True

    image_size = EfficientNet.get_image_size(model_name)
    tfms = transforms.Compose([
                transforms.Resize(image_size, interpolation=Image.BICUBIC),
                transforms.CenterCrop(image_size),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
    img = tfms(img).unsqueeze(0)

    # 训练得到结果

    # switch to train mode
    model.train()
    with torch.no_grad():
        logits = model(img.cuda())
    preds = torch.topk(logits, k=5)[1].squeeze(0).tolist()
    print('-----')
    for idx in preds:
        label = labels_map[idx]
        prob = torch.softmax(logits, dim=1)[0, idx].item()
        print('{:<75} ({:.2f}%)'.format(label, prob * 100))


if __name__ == '__main__':
    img = Image.open("./data_processing/datasets/training/extracted/00001.jpg")
    tell(img)
