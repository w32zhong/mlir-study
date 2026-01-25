## PyTorch
Download:
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

Build:
```sh
rm -rf ./build
CMAKE_ONLY=1 python setup.py build
cmake --build ./build --target install --config Release -j $((`nproc` - 2))
pip install --no-build-isolation -v -e . --config-settings editable_mode=compat
```

The `--config-settings editable_mode=compat` option is used for making my pyright LSP compatible with the [new editable install](https://setuptools.pypa.io/en/latest/userguide/development_mode.html).

## LLVM
Download (see Triton Section for the commit SHA1):
```sh
wget https://github.com/llvm/llvm-project/archive/{commit}.tar.gz -O llvm-project.tar.gz
tar xzf llvm-project.tar.gz -C llvm-project --strip-components=1
```

Build:
```sh
cmake -S ./llvm-project/llvm -B ./llvm-project/build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_PROJECTS="clang;lld;lldb;clang-tools-extra;mlir" \
    -DLLVM_BUILD_EXAMPLES=ON \
    -DLLVM_TARGETS_TO_BUILD="Native;NVPTX" # add AMDGPU to support AMD

ninja -C ./llvm-project/build -j $((`nproc` - 2))
```

[Toy Tutorial](https://mlir.llvm.org/docs/Tutorials/Toy/):
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

To install binary to the pixi environment:
```sh
cmake --install llvm-project/build --prefix ./.pixi/envs/default
```

## Triton
Download:
```sh
git clone -b v3.6.0 --depth 1 git@github.com:triton-lang/triton.git
cd triton

```

Uncomment AMD targets in `CMakeLists.txt`:
```
    #LLVMAMDGPUCodeGen
    #LLVMAMDGPUAsmParser
```

Determine the LLVM version SHA1 to match Triton:
```sh
cat cmake/llvm-hash.txt
f6ded0be897e2878612dd903f7e8bb85448269e5
```

Build:
```sh
export LLVM_BUILD_DIR=$(readlink -f ../llvm-project/build)
export LLVM_INCLUDE_DIRS=${LLVM_BUILD_DIR}/include
export LLVM_LIBRARY_DIR=${LLVM_BUILD_DIR}/lib
export LLVM_SYSPATH=${LLVM_BUILD_DIR}
# pip editable build trigers `develop` (deprecated) or `editable_wheel` (PEP 660)
pip install --no-build-isolation -v -e . --config-settings editable_mode=compat
# alternatively, call setuptools super().run() `editable_wheel` (it will run `build_ext`)
python setup.py clean
python setup.py editable_wheel
```

## Toy Example
```py
import torch

def graph_break(a, b):
    x = a / (torch.abs(a) + 1)
    if b.sum() < 0:
        b = b * -1
    return x * b

def kernel_fusion(x, y):
    z = torch.matmul(x, y)
    return torch.nn.functional.softmax(z, dim=1)

def 2in1(a, b):
    c = graph_break(a, b)
    d = kernel_fusion(a, b)
    return c + d

if __name__ == '__main__':
    jit_2in1 = torch.compile(2in1)
    a = torch.rand((10, 10), device='cuda')
    b = torch.rand((10, 10), device='cuda')
    print(jit_2in1(a, b))
```

```sh
cd test

python test_install.py # test our install

# now, run a toy torch-compile program
rm -rf ./torch_compile_debug
export TORCHINDUCTOR_FORCE_DISABLE_CACHES=1 # force re-JIT
export TORCH_COMPILE_DEBUG=1 # generate ./torch_compile_debug
CUDA_VISIBLE_DEVICES=0 python test_torch_compile.py
```
