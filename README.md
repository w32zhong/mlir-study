# LLVM
A stripped [LLVM project](https://github.com/llvm/llvm-project),
commit: `b76089c7f3d6593d2e2c83db7dbf4965b656bd8c`
(this commit is selected to align [Modular code](https://github.com/modular/modular/blob/main/MODULE.bazel)).

## Download
```sh
wget https://github.com/llvm/llvm-project/archive/{}.tar.gz
tar xzf b76089c7f3d6593d2e2c83db7dbf4965b656bd8c.tar.gz -C llvm-project --strip-components=1
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
wget https://github.com/pytorch/pytorch/releases/download/v2.8.0/pytorch-v2.8.0.tar.gz
tar xzf pytorch-v2.8.0.tar.gz -C pytorch --strip-components=1
```
