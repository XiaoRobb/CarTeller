import torch as t
import torch.nn as nn
from torchvision import models, transforms
from torch.utils.data import DataLoader, Dataset
from torch.autograd import Variable
from PIL import Image
import io

batch_size = 1
num_classes = 5
learning_rate = 0.0002
model_path = "../checkpoints/vgg.pth"
use_gpu = t.cuda.is_available()
print(use_gpu)
car_types = ["Bus", "Car", "Truck", "Motorcycle", "Tricycle"]
test_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.RandomResizedCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


class CarTypeTeller:
    @staticmethod
    def tell(imgs):
        test_datasets = TsetDataSet(imgs, test_transforms)
        test_dataloader = DataLoader(test_datasets, batch_size=batch_size)

        model = VGGNet()
        if use_gpu:
            model.load_state_dict(t.load(model_path))
            model.cuda()
        else:
            model = t.nn.DataParallel(model)
            model.load_state_dict(t.load(model_path, map_location="cpu"))

        # 测试
        model.eval()
        outcome = []
        for batch_x in test_dataloader:
            if use_gpu:
                with t.no_grad():
                    batch_x = Variable(batch_x).cuda()
            else:
                with t.no_grad():
                    batch_x = Variable(batch_x)
            out = model(batch_x)
            pred = t.max(out, 1)[1]
            pred_types = pred.data.cpu().numpy().tolist()
            outcome.append(car_types[pred_types[0]])
        final_str = ""
        for str in outcome:
            final_str += str
        return  final_str


class TsetDataSet(Dataset):
    def __init__(self, imgs, transform):
        self.transform = transform
        self.imgs = imgs

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, index):
        image = self.imgs[index]
        image = self.transform(image)
        return image


class VGGNet(nn.Module):
    def __init__(self):
        super(VGGNet, self).__init__()
        net = models.vgg16(pretrained=True)
        net.classifier = nn.Sequential()
        self.features = net
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 512),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(512, 128),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x





if __name__ == "__main__":
    img = Image.open(r"D:\AllProjects\Pytorch\CarTypeTeller\data\test\3.jpg")
    imgs = [img]
    print(CarTypeTeller.tell(imgs))

