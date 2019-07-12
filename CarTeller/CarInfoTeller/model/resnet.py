import torch.nn as nn
from torchvision.models import resnet34, resnet18, resnet50 , resnet101, resnet152
from CarInfoTeller.base import BaseModel


class ResNet152(BaseModel):

    def __init__(self, num_classes=196, use_pretrained=True):
        super(BaseModel, self).__init__()
        self.model = resnet152(pretrained=use_pretrained)

        # replace last layer with total cars classes
        n_inputs = self.model.fc.in_features
        classifier = nn.Sequential(nn.Linear(n_inputs, num_classes))
        self.model.fc = classifier

    def forward(self, x):

        return self.model(x)


class ResNet101(BaseModel):

    def __init__(self, num_classes=196, use_pretrained=True):
        super(BaseModel, self).__init__()
        self.model = resnet101(pretrained=use_pretrained)

        # replace last layer with total cars classes
        n_inputs = self.model.fc.in_features
        classifier = nn.Sequential(nn.Linear(n_inputs, num_classes))
        self.model.fc = classifier

    def forward(self, x):

        return self.model(x)


class ResNet50(BaseModel):

    def __init__(self, num_classes=196, use_pretrained=True):
        super(BaseModel, self).__init__()
        self.model = resnet50(pretrained=use_pretrained)

        # replace last layer with total cars classes
        n_inputs = self.model.fc.in_features
        classifier = nn.Sequential(nn.Linear(n_inputs, num_classes))
        self.model.fc = classifier

    def forward(self, x):

        return self.model(x)


class ResNet34(BaseModel):

    def __init__(self, num_classes=196, use_pretrained=True):
        super(BaseModel, self).__init__()
        self.model = resnet34(pretrained=use_pretrained)

        # replace last layer with total cars classes
        n_inputs = self.model.fc.in_features
        classifier = nn.Sequential(nn.Linear(n_inputs, num_classes))
        self.model.fc = classifier

    def forward(self, x):

        return self.model(x)


class ResNet18(BaseModel):

    def __init__(self, num_classes=196, use_pretrained=True):
        super(BaseModel, self).__init__()
        self.model = resnet18(pretrained=use_pretrained)

        # replace last layer with total cars classes
        n_inputs = self.model.fc.in_features
        classifier = nn.Sequential(nn.Linear(n_inputs, num_classes))
        self.model.fc = classifier

    def forward(self, x):

        return self.model(x)
