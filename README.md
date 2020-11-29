# rlfuzz

Inspired by [gym_fuzz1ng](https://github.com/spolu/gym_fuzz1ng)

## Installation

```sh
# tested in Ubuntu 16.04.6
# for LAVA-M
sudo apt install libacl1 libacl1-dev

# for AFL
sudo sh -c "echo core > /proc/sys/kernel/core_pattern"

for i in `ls /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor` ; do sudo sh -c "echo performance > $i"; done

# install rlfuzz, testeded in Python 3.8.5
pip install .

# open main.ipynb in ./examples with jupyter, it's a simple test for DDPGAgent
```

## Add New Environments

* modify `rlfuzz/setup.py` to add new target binary in `package_data`.
* modify `rlfuzz/rlfuzz/__init__.py` to register new envs.
* modify `rlfuzz/rlfuzz/envs/__init__.py` to import new env class defined in `rlfuzz/rlfuzz/envs/fuzz_lava_m_env.py`.
* modify `rlfuzz/rlfuzz/mods/Makefile` to generate new target binary in `rlfuzz/rlfuzz/mods/lava-m-mod/`.
