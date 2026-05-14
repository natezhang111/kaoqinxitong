from __future__ import annotations

from collections import OrderedDict
from pathlib import Path
from typing import Tuple

import torch
import torch.nn as nn
import torch.nn.init as init
from torch.nn import functional as F
from torchvision import models


def _build_resnet18(pretrained: bool) -> nn.Module:
    try:
        backbone = models.resnet18(weights=None)
    except TypeError:
        backbone = models.resnet18(pretrained=False)

    if not pretrained:
        return backbone

    msceleb_checkpoint = Path(__file__).resolve().parents[2] / "models" / "emotion" / "resnet18_msceleb.pth"
    if msceleb_checkpoint.exists():
        checkpoint = torch.load(str(msceleb_checkpoint), map_location="cpu", weights_only=False)
        state_dict = checkpoint.get("state_dict", checkpoint)
        backbone.load_state_dict(state_dict, strict=True)
        return backbone

    try:
        return models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    except AttributeError:
        return models.resnet18(pretrained=True)


class SpatialAttention(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1x1 = nn.Sequential(
            nn.Conv2d(512, 256, kernel_size=1),
            nn.BatchNorm2d(256),
        )
        self.conv_3x3 = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
        )
        self.conv_1x3 = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=(1, 3), padding=(0, 1)),
            nn.BatchNorm2d(512),
        )
        self.conv_3x1 = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=(3, 1), padding=(1, 0)),
            nn.BatchNorm2d(512),
        )
        self.relu = nn.ReLU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y = self.conv1x1(x)
        y = self.relu(self.conv_3x3(y) + self.conv_1x3(y) + self.conv_3x1(y))
        y = y.sum(dim=1, keepdim=True)
        return x * y


class ChannelAttention(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.gap = nn.AdaptiveAvgPool2d(1)
        self.attention = nn.Sequential(
            nn.Linear(512, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(inplace=True),
            nn.Linear(32, 512),
            nn.Sigmoid(),
        )

    def forward(self, sa: torch.Tensor) -> torch.Tensor:
        pooled = self.gap(sa)
        pooled = pooled.view(pooled.size(0), -1)
        weights = self.attention(pooled)
        return pooled * weights


class CrossAttentionHead(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.sa = SpatialAttention()
        self.ca = ChannelAttention()
        self.init_weights()

    def init_weights(self) -> None:
        for module in self.modules():
            if isinstance(module, nn.Conv2d):
                init.kaiming_normal_(module.weight, mode="fan_out")
                if module.bias is not None:
                    init.constant_(module.bias, 0)
            elif isinstance(module, nn.BatchNorm2d):
                init.constant_(module.weight, 1)
                init.constant_(module.bias, 0)
            elif isinstance(module, nn.Linear):
                init.normal_(module.weight, std=0.001)
                if module.bias is not None:
                    init.constant_(module.bias, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.ca(self.sa(x))


class DAN(nn.Module):
    def __init__(self, num_class: int = 8, num_head: int = 4, pretrained: bool = False) -> None:
        super().__init__()
        backbone = _build_resnet18(pretrained=pretrained)
        self.features = nn.Sequential(*list(backbone.children())[:-2])
        self.num_head = num_head
        for index in range(num_head):
            setattr(self, f"cat_head{index}", CrossAttentionHead())
        self.sig = nn.Sigmoid()
        self.fc = nn.Linear(512, num_class)
        self.bn = nn.BatchNorm1d(num_class)

    def _head_modules(self) -> list[CrossAttentionHead]:
        return [getattr(self, f"cat_head{index}") for index in range(self.num_head)]

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        features = self.features(x)
        head_outputs = [head(features) for head in self._head_modules()]
        heads = torch.stack(head_outputs).permute(1, 0, 2)
        if heads.size(1) > 1:
            heads = F.log_softmax(heads, dim=1)
        logits = self.fc(heads.sum(dim=1))
        logits = self.bn(logits)
        return logits, features, heads


def sanitize_state_dict(raw_state_dict: OrderedDict | dict) -> OrderedDict:
    state_dict = OrderedDict()
    for key, value in raw_state_dict.items():
        normalized_key = str(key)
        if normalized_key.startswith("module."):
            normalized_key = normalized_key[7:]
        if normalized_key.startswith("model."):
            normalized_key = normalized_key[6:]
        state_dict[normalized_key] = value
    return state_dict
