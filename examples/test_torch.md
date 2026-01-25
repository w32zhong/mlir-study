## Quick C++ Changes without `pip install`
Normally, you will need `pip install` to copy library binary from `./build` to `./torch` to reflect changes in a `csrc` file.

`pip install` also add `stub.o` to the compiled library and generate `_C.*.so`, i.e., `torch._C`:
```txt
  building 'torch._C' extension
  gcc *** torch/csrc/stub.c -ltorch_python -o torch/_C.cpython-313-x86_64-linux-gnu.so
```

To avoid `pip install`, we can create a symbolic link per the instructions from the [offical PyTorch repo](https://github.com/pytorch/pytorch/blob/main/CONTRIBUTING.md#tips-and-debugging):
```sh
torch/lib; ln -sf ../../build/lib/libtorch* .; popd
```

Now, simply rebuild C++ source can reflect the changes:
```sh
ninja -C build install -j 2
```

You may notice that `torch/_C.cpython-313-x86_64-linux-gnu.so` isn't updated in this case.
This is because `torch/csrc/stub.c` only wraps the `initModule` in the `PyInit__C` Python entrance function which will be called during the first `import torch`;
it dynamically links to all PyTorch C functions via the ELF DT_NEEDED tags, e.g., `_C.*.so` needs `libtorch_python.so`.

Most likely, this thin wrapper does not need to be re-compiled.
The actual entrance definition is defined in `libtorch_python.so`
```sh
$ nm --extern-only --demangle --defined-only --line-numbers torch/_C.*.so | grep initModule
# nothing will show up here
$ nm --extern-only --demangle --defined-only torch/lib/libtorch_python.so | grep initModule
0000000000937287 T initModule
```

## Attaching a Debugger
To set up a breakpoint in a C++ source file after some Python code,
we can insert a `breakpoint()` in Python:
```py
import os; print(os.getpid())
breakpoint()
```
and attach a gdb/lldb debugger to it:
```sh
sudo bash -c 'echo 0 > /proc/sys/kernel/yama/ptrace_scope'
gdb -p <pid> python
(gdb) break THPVariable_rand
(gdb) c
```
then switch back to Python.
