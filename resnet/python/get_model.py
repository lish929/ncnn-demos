import torch
import torchvision

def get_resnet18():
    model = torchvision.models.resnet18(pretrained=True)
    torch.save(model,"../models/resnet_18.pt")
    return model

if __name__ == "__main__":
    model = get_resnet18()
    print(model)