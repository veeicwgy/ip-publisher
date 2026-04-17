from __future__ import annotations

import subprocess
import sys

packages = [
    'pyyaml',
    'requests',
]

for package in packages:
    subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)

print('Python dependencies installed successfully.')
