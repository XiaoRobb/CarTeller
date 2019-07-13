"""
Evaluate on ImageNet. Note that at the moment, training is not implemented (I am working on it).
that being said, evaluation is working.
"""

import argparse
import shutil
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
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

    # switch to train mode
    model.train()

    train_loss = 0.
    train_acc = 0.
    all_num = len(train_loader)
    for i, (images, target) in enumerate(train_loader):
        # measure data loading time

        target = target.cuda()

        # compute output
        output = model(images.cuda())
        loss = criterion(output, target)
        train_loss += loss.item()

        pred = torch.max(output, 1)[1]
        train_correct = (pred == target).sum()
        train_acc += train_correct.item()

        # compute gradient and do SGD step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if i % opt_train.print_freq == 0:
            print('Train: Epoch[{}] [{}/{}] Loss:{:.6f}, Acc:{:.6f}'
                  .format(epoch, i, all_num, train_loss / all_num, train_acc / ((i+1) * opt_train.batch_size)))
    print('***Train: Epoch[{}] Loss:{:.6f}, Acc:{:.6f}'
          .format(epoch, train_loss / all_num, train_acc / (all_num * opt_train.batch_size)))


def validate(val_loader, model, criterion):

    # switch to evaluate mode
    model.eval()
    val_loss = 0.
    val_acc = 0.
    all_num = len(val_loader)
    with torch.no_grad():
        for i, (images, target) in enumerate(val_loader):
            if opt_train.use_gpu:
                images = images.cuda()
                target = target.cuda()

            # compute output
            output = model(images)
            loss = criterion(output, target)

            val_loss += loss.item()

            pred = torch.max(output, 1)[1]
            val_correct = (pred == target).sum()
            val_acc += val_correct.item()
            if i % opt_train.print_freq == 0:
                print('Val: [{}/{}] Loss:{:.6f}, Acc:{:.6f}'
                      .format(i, all_num, val_loss / all_num, val_acc / ((i+1) * opt_train.batch_size)))
    print('***Val: Loss:{:.6f}, Acc:{:.6f}'.format(val_loss / all_num, val_acc / (all_num * opt_train.batch_size)))

    return val_acc


def save_checkpoint(state, is_best, filename='./checkpoints/checkpoint.pth.tar'):
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, './checkpoints/model_best.pth.tar')


def adjust_learning_rate(optimizer, epoch):
    """Sets the learning rate to the initial LR decayed by 10 every 30 epochs"""
    lr = opt_train.lr * (0.1 ** (epoch // 30))
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr





if __name__ == '__main__':
    work()
