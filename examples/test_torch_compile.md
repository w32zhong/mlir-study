```sh
cd test
rm -rf ./torch_compile_debug
export TORCHINDUCTOR_FORCE_DISABLE_CACHES=1 # force re-JIT
export TORCH_COMPILE_DEBUG=1 # generate ./torch_compile_debug
CUDA_VISIBLE_DEVICES=0 python test_torch_compile.py
```
