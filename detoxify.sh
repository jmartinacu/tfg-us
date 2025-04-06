#!/bin/bash

SCRIPT_DIR=$(cd -- "$(dirname -- ${BASH_SOURCE[0]})" &> /dev/null && pwd)

MODEL_FILE="multilingual_debiased-0b549669.ckpt"

MODEL_URL="https://github.com/unitaryai/detoxify/releases/download/v0.4-alpha/${MODEL_FILE}"

if [[ ! -f "${SCRIPT_DIR}/torch_model_cache/${MODEL_FILE}" ]]; then
  echo "Downloading detoxify model"
  mkdir -p "${SCRIPT_DIR}/torch_model_cache"
  curl -L -o "${SCRIPT_DIR}/torch_model_cache/${MODEL_FILE}" "${MODEL_URL}"
fi