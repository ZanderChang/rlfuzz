import os

from gym.envs.registration import register

def afl_forkserver_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/afl-2.52b-mod/afl-2.52b/afl-forkserver',
    )

# base64_afl
def base64_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/lava-m-mod/base64_afl',
    )

register(
    id='FuzzBase64-v0',
    entry_point='rlfuzz.envs:FuzzBase64Env',
)

# md5sum_afl
def md5sum_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/lava-m-mod/md5sum_afl',
    )

register(
    id='FuzzMd5sum-v0',
    entry_point='rlfuzz.envs:FuzzMd5sumEnv',
)

# uniq_afl
def uniq_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/lava-m-mod/uniq_afl',
    )

register(
    id='FuzzUniq-v0',
    entry_point='rlfuzz.envs:FuzzUniqEnv',
)

# who_afl
def who_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/lava-m-mod/who_afl',
    )

register(
    id='FuzzWho-v0',
    entry_point='rlfuzz.envs:FuzzWhoEnv',
)