import subprocess
import sys

from setuptools import setup
from distutils.command.build import build as DistutilsBuild


class Build(DistutilsBuild):
    def run(self):
        try:
            subprocess.check_call(['make', 'all'], cwd='rlfuzz/mods')
        except subprocess.CalledProcessError as e:
            sys.stderr.write("Could not build mods: %s.\n" % e)
            raise
        DistutilsBuild.run(self)


setup(
    name='rlfuzz',
    version='1.0.0',
    platforms='Posix',
    install_requires=[
        'gym>=0.10.3',
        'xxhash>=1.0.1',
        'posix_ipc>=1.0.3',
    ],
    author='adbq, spolu, zheng',
    package_data={
        'rlfuzz.mods': [
            'afl-2.52b-mod/afl-2.52b/afl-forkserver',
            'lava-m-mod/base64_afl',
            'lava-m-mod/md5sum_afl',
            'lava-m-mod/uniq_afl',
            'lava-m-mod/who_afl',
        ],
        'rlfuzz.envs': ['config.ini']
    },
    packages=[
        'rlfuzz',
        'rlfuzz.coverage',
        'rlfuzz.mods',
        'rlfuzz.envs',
    ],
    cmdclass={'build': Build},
    include_package_data=True
)
