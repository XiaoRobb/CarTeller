import cv2
import torch
from scipy import io as mat_io
from skimage import io
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image


class CarsDataset(Dataset):
    """
        Cars Dataset
    """
    def __init__(self, mode, data_dir, image_size):

        self.data_dir = data_dir
        self.img_names = []
        self.target = []

        self.mode = mode
        if mode == "test":
            metas = data_dir + "cars_metas/cars_test_annos"
        else:
            metas = data_dir + "cars_metas/cars_train_annos"

        labels_meta = mat_io.loadmat(metas)
        for img_ in labels_meta['annotations'][0]:
            if mode == "test":
                self.img_names.append(img_[4][0])
            else:
                self.img_names.append(img_[5][0])
                self.target.append(img_[4][0][0])
        if self.mode == "train":
            self.train_transform = transforms.Compose([
                transforms.RandomResizedCrop(224),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
        else:
            self.val_or_test_transform = transforms.Compose([
                transforms.Resize(image_size, interpolation=Image.BICUBIC),
                transforms.CenterCrop(image_size),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])

        if self.mode == "train":
            self.img_names = self.img_names[:int(0.8 * len(self.img_names))]
            self.target = self.target[:int(0.8 * len(self.target))]
        elif self.mode == "val":
            self.img_names = self.img_names[int(0.8 * len(self.img_names)):]
            self.target = self.target[int(0.8 * len(self.target)):]

    def __getitem__(self, index):
        if self.mode == "test":
            img_path = self.data_dir + "testing/extracted/" + self.img_names[index]
        else:
            img_path = self.data_dir + "training/extracted/" + self.img_names[index]
        image = Image.open(img_path)
        image = image.convert('RGB')
        if self.mode == 'train':
            return self.train_transform(image), torch.tensor(self.target[index]-1, dtype=torch.long)
        elif self.mode == 'val':
            return self.val_or_test_transform(image), torch.tensor(self.target[index] - 1, dtype=torch.long)
        elif self.mode == 'test':
            return self.val_or_test_transform(image), torch.tensor(-1, dtype=torch.long)

    def __len__(self):
        return len(self.img_names)


