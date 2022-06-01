#!/bin/bash

VENV_DIR=venv
PYTHON=python3

if [[ ! -d venv ]]; then
    echo "Installing virtual environment"
    $PYTHON -m venv $VENV_DIR
fi

echo "Activate vitual environment:"
echo "  source $VENV_DIR/bin/activate"
echo "  ./install-requirements.sh"
