cd third_party/pthreadpool
git fetch origin d90cd6f1493e09d12c407243f7f331a8cda55efb
git checkout d90cd6f1493e09d12c407243f7f331a8cda55efb

cd third_party/FP16
git fetch --unshallow
git checkout 4987f20d48c22694d84bbffa839168596ea027ae

pip install -e ./third_party/python-peachpy
