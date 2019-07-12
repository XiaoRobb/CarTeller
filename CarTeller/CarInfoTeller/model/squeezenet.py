import torch.nn as nn
from torchvision.models import squeezenet
from CarInfoTeller.base import BaseModel


class SqueezeNet(BaseModel):
    def __init__(self, num_classes=196, use_pretrained=False):
        super(BaseModel, self).__init__()
        self.model = squeezenet.squeezenet1_0(pretrained=use_pretrained)

        self.model.num_classes = num_classes

        # # replace last layer with total cars classes
        self.model.classifier[1] = nn.Conv2d(512, num_classes, kernel_size=(1, 1), stride=(1, 1))

    def forward(self, x):
        return self.model.forward(x)
