# LLVM
A stripped [LLVM project](https://github.com/llvm/llvm-project),
commit: `b76089c7f3d6593d2e2c83db7dbf4965b656bd8c`
(this commit is selected to align [Modular code](https://github.com/modular/modular/blob/main/MODULE.bazel)).

## Download
```sh
wget https://github.com/llvm/llvm-project/archive/{commit}.tar.gz -O llvm-project.tar.gz
tar xzf llvm-project.tar.gz -C llvm-project --strip-components=1
```

## Build
```sh
cmake -S ./llvm-project/llvm -B ./llvm-project/build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_PROJECTS="clang;lld;lldb;clang-tools-extra;mlir" \
    -DLLVM_BUILD_EXAMPLES=ON \
    -DLLVM_TARGETS_TO_BUILD="Native;NVPTX"

ninja -C ./llvm-project/build -j $((`nproc` - 2))
```

## [Toy Tutorial](https://mlir.llvm.org/docs/Tutorials/Toy/)
```sh
./build/bin/clang++ -g \
    -o build/toyc.bin \
    llvm-project/mlir/examples/toy/Ch1/toyc.cpp \
    llvm-project/mlir/examples/toy/Ch1/parser/AST.cpp \
    -I llvm-project/mlir/examples/toy/Ch1/include \
    $(build/bin/llvm-config --cxxflags --ldflags --libs core support native --system-libs)

./build/toyc.bin llvm-project/mlir/test/Examples/Toy/Ch1/ast.toy -emit=ast
```

lldb usage example:
```sh
./build/bin/lldb ./build/toyc.bin
(lldb) b Parser.h:42
(lldb) r llvm-project/mlir/test/Examples/Toy/Ch1/ast.toy -emit=ast
(lldb) f # frame
(lldb) expr auto t = lexer.getNextToken(); t;
(lldb) p lexer.curTok
(lldb) c # continue
```

# PyTorch
## Download
```sh
# pytorch requires git repo to know the exact versions of 3rd_party dependencies
rm -rf pytorch
git clone -b v2.10.0 --depth 1 https://github.com/pytorch/pytorch pytorch
git checkout ./pytorch/.keep
cd pytorch

# download pytorch submodules
git submodule update --init --recursive

# Optional: backup at this point in case of a fresh rebuild.
```

## Build
```sh
rm -rf ./build
CMAKE_ONLY=1 python setup.py build
cmake --build ./build --target install --config Release -j $((`nproc` - 2))
```

## Toy Example
```py
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
```

```sh
rm -rf ./torch_compile_debug
export TORCHINDUCTOR_FORCE_DISABLE_CACHES=1 # force re-JIT
export TORCH_COMPILE_DEBUG=1 # generate ./torch_compile_debug
CUDA_VISIBLE_DEVICES=0 python tmp/fusion2.py
```
