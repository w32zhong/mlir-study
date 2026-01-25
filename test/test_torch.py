import torch
print('Torch path:', torch.__path__)
print('Torch version:', torch.__version__)
print('CUDA:', torch.cuda.is_available())
print('CUDA version:', torch.version.cuda)

