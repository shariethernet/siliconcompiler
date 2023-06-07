#!/bin/bash

cd /workspace/siliconcompiler
python3 -m pip install --upgrade -e .
export SCPATH=/workspace/siliconcompiler/siliconcompiler 

exec "$@"

