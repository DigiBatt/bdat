#! /bin/bash

cd "$(dirname $(readlink -f $0))"
mkdir -p ./out
find ./src -name '*.py' -exec bash -c 'python $0 > ./out/$(basename $0 .py).json' {} \;
