#!/bin/bash
set -a
. .secrets
set +a
python -m app.bot
