import rlfuzz
from rlfuzz.envs.fuzz_base_env import FuzzBaseEnv

import os

class FuzzUserDefinedEnv(FuzzBaseEnv):
    def __init__(self):
        print('[+] Use AFL-2.25b to compile your source code')
        print('[+] Input binary loction:')
        self._target_path = input()
        assert os.path.isfile(self._target_path)
        print(self._target_path)

        print('[+] Input args (default empty):')
        self._args = input().split()
        if not self._args:
            self._args = []
        print(self._args)

        print('[+] Input max size of input (in bytes, default 32 * 1024):')
        self._input_maxsize = input()
        self._input_maxsize = 32 * 1024 if not self._input_maxsize else int(self._input_maxsize)
        print(self._input_maxsize)

        print('[+] No initial seed.')
        self._seed = b''  # 指定初始变异的文件

        super(FuzzUserDefinedEnv, self).__init__()
    
    def set_seed(self, seed):
        assert len(seed) > 0
        assert isinstance(seed, bytes)
        self._seed = seed
        self._input_maxsize = len(seed)
        self.reset()