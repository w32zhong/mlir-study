import torch

def toy_graph_break(a, b):
    x = a / (torch.abs(a) + 1)
    if b.sum() < 0:
        b = b * -1
    return x * b

def toy_kernel_fusion(x, y):
    z = torch.matmul(x, y)
    return torch.nn.functional.softmax(z, dim=1)

def toy_2in1(a, b):
    c = toy_graph_break(a, b)
    d = toy_kernel_fusion(a, b)
    return c + d

if __name__ == '__main__':
    jit_toy_2in1 = torch.compile(toy_2in1)
    a = torch.rand((10, 10), device='cuda')
    b = torch.rand((10, 10), device='cuda')
    print(jit_toy_2in1(a, b))
