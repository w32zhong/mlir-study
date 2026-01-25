import torch
import triton
print('Triton path:', triton.__path__)

import triton.language as tl

@triton.jit
def plus_one_kernel(
        x_ptr,
        N: tl.constexpr,
        M: tl.constexpr,
        BLOCK_N: tl.constexpr,
        BLOCK_M: tl.constexpr,
    ):
    n_id = tl.program_id(0)
    m_id = tl.program_id(1)
    row_offset = tl.arange(0, BLOCK_N) + n_id * BLOCK_N
    col_offset = tl.arange(0, BLOCK_M) + m_id * BLOCK_M
    index = row_offset[:, None] * M + col_offset[None, :]
    block_ptr = x_ptr + index
    mask = (row_offset[:, None] < N) & (col_offset[None, :] < M)
    x = tl.load(block_ptr, mask=mask)
    tl.store(block_ptr, x + 1, mask=mask)

N = 16  # Number of rows
M = 32  # Number of columns
BLOCK_N = 8  # Block size in rows
BLOCK_M = 16  # Block size in columns
x = torch.ones((N, M), dtype=torch.float32, device='cuda')
plus_one_kernel[(N // BLOCK_N, M // BLOCK_M)](x, N, M, BLOCK_N, BLOCK_M)
print("Output Tensor:\n", x)
