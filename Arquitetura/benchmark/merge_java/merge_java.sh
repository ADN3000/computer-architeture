#!/bin/bash
set -e
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
exec java -cp "$ROOT/bin" MergeSort
