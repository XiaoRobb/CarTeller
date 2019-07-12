import torch.nn as nn
from torchvision.models import inception_v3
from CarInfoTeller.base import BaseModel


class InceptionV3(BaseModel):

    def __init__(self, num_classes=196, use_pretrained=True):
        super(BaseModel, self).__init__()
        self.model = inception_v3(pretrained=use_pretrained)

        n_inputs = self.model.fc.in_features
        classifier = nn.Sequential(nn.Linear(n_inputs, num_classes))
        self.model.fc = classifier

    def forward(self, x):
        return self.model(x)
