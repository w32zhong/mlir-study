A stripped [LLVM project](https://github.com/llvm/llvm-project), commit: b76089c7f3d6593d2e2c83db7dbf4965b656bd8c

## Download
```sh
wget https://github.com/llvm/llvm-project/archive/{}.tar.gz
tar xzf b76089c7f3d6593d2e2c83db7dbf4965b656bd8c.tar.gz -C llvm-project --strip-components=1
```

## Build
```
cmake -S llvm -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_PROJECTS="clang;lld;lldb;clang-tools-extra" \
    -DLLVM_ENABLE_PROJECTS=mlir \
    -DLLVM_BUILD_EXAMPLES=ON \
    -DLLVM_TARGETS_TO_BUILD="Native;NVPTX"

ninja -C build -j 12
```
