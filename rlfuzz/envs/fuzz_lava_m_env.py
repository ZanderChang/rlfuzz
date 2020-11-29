import rlfuzz
from rlfuzz.envs.fuzz_base_env import FuzzBaseEnv

import os

class FuzzBase64Env(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.base64_target_path()
        self._args = ['-d']
        self._seed = b''  # 指定初始变异的文件
        self._input_maxsize = 32 * 1024 # 最大输入文件的大小 
        super(FuzzBase64Env, self).__init__()
    
    def set_seed(self, seed):
        assert len(seed) > 0
        assert isinstance(seed, bytes)
        self._seed = seed
        self._input_maxsize = len(seed)
        self.reset()

class FuzzMd5sumEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.md5sum_target_path()
        self._args = ['-c']
        self._seed = b''  # 指定初始变异的文件
        self._input_maxsize = 32 * 1024 # 最大输入文件的大小 
        super(FuzzMd5sumEnv, self).__init__()

    def set_seed(self, seed):
        assert len(seed) > 0
        assert isinstance(seed, bytes)
        self._seed = seed
        self._input_maxsize = len(seed)
        self.reset()

class FuzzUniqEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.uniq_target_path()
        self._args = []
        self._seed = b''  # 指定初始变异的文件
        self._input_maxsize = 32 * 1024 # 最大输入文件的大小 
        super(FuzzUniqEnv, self).__init__()

    def set_seed(self, seed):
        assert len(seed) > 0
        assert isinstance(seed, bytes)
        self._seed = seed
        self._input_maxsize = len(seed)
        self.reset()

class FuzzWhoEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.who_target_path()
        self._args = []
        self._seed = b''  # 指定初始变异的文件
        self._input_maxsize = 32 * 1024 # 最大输入文件的大小 
        super(FuzzWhoEnv, self).__init__()

    def set_seed(self, seed):
        assert len(seed) > 0
        assert isinstance(seed, bytes)
        self._seed = seed
        self._input_maxsize = len(seed)
        self.reset()