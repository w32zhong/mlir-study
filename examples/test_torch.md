## Use rebuild changes without `pip install`
Normally, you will need `pip install` to copy library binary from `./build` to `./torch` to reflect changes in a `csrc` file.

To avoid `pip install`, we can create a symbolic link per the instructions from the [offical PyTorch repo](https://github.com/pytorch/pytorch/blob/main/CONTRIBUTING.md#tips-and-debugging):
```sh
cd torch
ln -sf ../build/lib.linux-x86_64-cpython-39/torch/_C.cpython-39-x86_64-linux-gnu.so .
cd -
ninja -C build install
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
