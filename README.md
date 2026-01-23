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
cmake -S ./llvm-project/llvm -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_PROJECTS="clang;lld;lldb;clang-tools-extra;mlir" \
    -DLLVM_BUILD_EXAMPLES=ON \
    -DLLVM_TARGETS_TO_BUILD="Native;NVPTX"

ninja -C build -j 12
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
wget https://github.com/pytorch/pytorch/archive/refs/tags/v2.10.0.tar.gz -O pytorch.tar.gz
tar xzf pytorch.tar.gz -C pytorch --strip-components=1
```

## Build
```sh
STUDY_ROOT=$(pwd)
cd pytorch
$STUDY_ROOT/scripts/git_submodule_update.sh
# optional: backup these third_party/* in case of a fresh rebuild.

rm -rf ./build
# a few cmake patches (on any error, search for "CMake Error")
cp ../pytorch_patch/cmake/*.cmake cmake/*.cmake
USE_SYSTEM_NCCL=0 CMAKE_ONLY=1 python setup.py build
cmake --build ./build --target install --config Release
```
