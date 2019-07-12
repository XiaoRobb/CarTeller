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
import PIL

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.optim
import torch.multiprocessing as mp
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
from efficientnet_pytorch import EfficientNet
from config import opt_train
from data_processing.car_dataset import CarsDataset
from torch.utils.data import DataLoader

parser = argparse.ArgumentParser(description='PyTorch ImageNet Training')
parser.add_argument('data', metavar='DIR',
                    help='path to dataset')
parser.add_argument('--resume', default='F', metavar='PATH',
                    help='path to latest checkpoint (default: none)')
args = parser.parse_args()


def work():

    print(opt_train.use_gpu)
    print(opt_train.num_classes)
    # 创建网络模型
    model = EfficientNet.from_pretrained(opt_train.model_name,num_classes=opt_train.num_classes)
    if opt_train.use_gpu:
        model.cuda()

    # 损失函数和优化器
    criterion = nn.CrossEntropyLoss().cuda()
    optimizer = torch.optim.SGD(model.parameters(), opt_train.lr,
                                momentum=opt_train.momentum,
                                weight_decay=opt_train.weight_decay)

    # 是否加载已有的模型
    if args.resume == 'T':
        print("=> loading checkpoint '{}'".format(opt_train.resume_file))
        checkpoint = torch.load(opt_train.resume_file)
        opt_train.start_epoch = checkpoint['epoch']
        opt_train.best_acc1 = checkpoint['best_acc1']
        model.load_state_dict(checkpoint['state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer'])
        print("=> loaded checkpoint '{}' (epoch {})".format(opt_train.resume_file, checkpoint['epoch']))

    cudnn.benchmark = True

    # 加载训练数据
    #    训练集
    train_dataset = CarsDataset('train', opt_train.data_dir, None)
    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=opt_train.batch_size, shuffle=True,
        num_workers=opt_train.num_wokers, pin_memory=True)

    #    验证集
    image_size = EfficientNet.get_image_size(opt_train.model_name)
    val_dataset = CarsDataset('val', opt_train.data_dir, image_size)
    val_loader = DataLoader(
        val_dataset,
        batch_size=opt_train.batch_size, shuffle=False,
        num_workers=opt_train.num_wokers, pin_memory=True)

    for epoch in range(opt_train.start_epoch, opt_train.epochs):
        adjust_learning_rate(optimizer, epoch)

        # train for one epoch
        train(train_loader, model, criterion, optimizer, epoch)

        # evaluate on validation set
        acc1 = validate(val_loader, model, criterion)

        # remember best acc@1 and save checkpoint
        is_best = acc1 > opt_train.best_acc1
        opt_train.best_acc1 = max(acc1, opt_train.best_acc1)
        print("save:", epoch)
        save_checkpoint({
            'epoch': epoch + 1,
            'state_dict': model.state_dict(),
            'best_acc1': opt_train.best_acc1,
            'optimizer': optimizer.state_dict(),
        }, is_best)


def train(train_loader, model, criterion, optimizer, epoch):
    batch_time = AverageMeter('Time', ':6.3f')
    data_time = AverageMeter('Data', ':6.3f')
    losses = AverageMeter('Loss', ':.4e')
    top1 = AverageMeter('Acc@1', ':6.2f')
    top5 = AverageMeter('Acc@5', ':6.2f')
    progress = ProgressMeter(len(train_loader), batch_time, data_time, losses, top1,
                             top5, prefix="Epoch: [{}]".format(epoch))

    # switch to train mode
    model.train()

    end = time.time()
    for i, (images, target) in enumerate(train_loader):
        # measure data loading time
        data_time.update(time.time() - end)

        target = target.cuda()

        # compute output
        output = model(images.cuda())
        loss = criterion(output, target)

        # measure accuracy and record loss
        acc1, acc5 = accuracy(output, target, topk=(1, 5))
        losses.update(loss.item(), images.size(0))
        top1.update(acc1[0], images.size(0))
        top5.update(acc5[0], images.size(0))

        # compute gradient and do SGD step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        if i % opt_train.print_freq == 0:
            progress.print(i)


def validate(val_loader, model, criterion):
    batch_time = AverageMeter('Time', ':6.3f')
    losses = AverageMeter('Loss', ':.4e')
    top1 = AverageMeter('Acc@1', ':6.2f')
    top5 = AverageMeter('Acc@5', ':6.2f')
    progress = ProgressMeter(len(val_loader), batch_time, losses, top1, top5,
                             prefix='Test: ')

    # switch to evaluate mode
    model.eval()

    with torch.no_grad():
        end = time.time()
        for i, (images, target) in enumerate(val_loader):
            if opt_train.use_gpu:
                images = images.cuda()
                target = target.cuda()

            # compute output
            output = model(images)
            loss = criterion(output, target)

            # measure accuracy and record loss
            acc1, acc5 = accuracy(output, target, topk=(1, 5))
            losses.update(loss.item(), images.size(0))
            top1.update(acc1[0], images.size(0))
            top5.update(acc5[0], images.size(0))

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            if i % opt_train.print_freq == 0:
                progress.print(i)

        # TODO: this should also be done with the ProgressMeter
        print(' * Acc@1 {top1.avg:.3f} Acc@5 {top5.avg:.3f}'
              .format(top1=top1, top5=top5))

    return top1.avg


def save_checkpoint(state, is_best, filename='./checkpoints/checkpoint.pth.tar'):
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, './checkpoints/model_best.pth.tar')


class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self, name, fmt=':f'):
        self.name = name
        self.fmt = fmt
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

    def __str__(self):
        fmtstr = '{name} {val' + self.fmt + '} ({avg' + self.fmt + '})'
        return fmtstr.format(**self.__dict__)


class ProgressMeter(object):
    def __init__(self, num_batches, *meters, prefix=""):
        self.batch_fmtstr = self._get_batch_fmtstr(num_batches)
        self.meters = meters
        self.prefix = prefix

    def print(self, batch):
        entries = [self.prefix + self.batch_fmtstr.format(batch)]
        entries += [str(meter) for meter in self.meters]
        print('\t'.join(entries))

    def _get_batch_fmtstr(self, num_batches):
        num_digits = len(str(num_batches // 1))
        fmt = '{:' + str(num_digits) + 'd}'
        return '[' + fmt + '/' + fmt.format(num_batches) + ']'


def adjust_learning_rate(optimizer, epoch):
    """Sets the learning rate to the initial LR decayed by 10 every 30 epochs"""
    lr = opt_train.lr * (0.1 ** (epoch // 30))
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


def accuracy(output, target, topk=(1,)):
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        # print("*********************************************************************")
        # print(pred)
        # print("*************")
        # print(target)
        # print(target.view(1, -1).expand_as(pred))
        correct = pred.eq(target.view(1, -1).expand_as(pred))
        # print(correct)
        # print("*********************************************************************")
        res = []
        for k in topk:
            correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))

        # print(res)
        return res


if __name__ == '__main__':
    work()
