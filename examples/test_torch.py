import torch
print('Torch path:', torch.__path__)
print('Torch version:', torch.__version__)
print('CUDA:', torch.cuda.is_available())
print('CUDA version:', torch.version.cuda)

import os; print(os.getpid())
breakpoint()

a = torch.rand((3, 4), device='cuda')
x = torch.abs(a).sum()
print(x)
