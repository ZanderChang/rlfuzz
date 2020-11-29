# 参考libfuzzer实现
# https://zanderchang.github.io/2019/12/11/libfuzzer%E4%B8%AD%E7%9A%84%E5%8F%98%E5%BC%82%E7%AD%96%E7%95%A5%E5%88%86%E6%9E%90/#more

from random import randint, shuffle
import struct

def Rand(a):
    if a == 0:
        return 0
    else:
        return randint(0, a-1) # [0, a-1]

def isdigit(a):
    return ord('0') <= a <= ord('9')

class FuzzMutator():
    def __init__(self, maxSize, userDict=None):
        self.maxSize = maxSize
        self.userDict = userDict
        self.funcMap = {
            0: self.Mutate_EraseBytes,
            1: self.Mutate_InsertByte,
            2: self.Mutate_InsertRepeatedBytes,
            3: self.Mutate_ChangeByte,
            4: self.Mutate_ChangeBit,
            5: self.Mutate_ShuffleBytes,
            6: self.Mutate_ChangeASCIIInteger,
            7: self.Mutate_ChangeBinaryInteger,
            8: self.Mutate_CopyPart,
            # 9: self.Mutate_Random
            # 9: self.Mutate_AddWordFromManualDictionary
        }
        self.methodNum = len(self.funcMap)
    
    def Mutate_Random(self, data):
        idx = Rand(self.methodNum - 1)
        return self.funcMap[idx](data)

    def Mutate_EraseBytes(self, data):
        if len(data) > 0:
            n = Rand(len(data) // 2) + 1
            s = Rand(len(data) - n + 1)
            return data[0:s] + data[s+n:]
        else:
            return data

    def Mutate_InsertByte(self, data):
        if len(data) >= self.maxSize:
            return data
        else:
            b = Rand(256)
            s = Rand(len(data) + 1)
            l = list(data)
            l.insert(s, b)
            return bytes(l)

    def Mutate_InsertRepeatedBytes(self, data):
        kMinBytesToInsert = 3
        if kMinBytesToInsert + len(data) >= self.maxSize:
            return data
        else:
            MaxBytesToInsert = min(self.maxSize - len(data), 128)
            repeatedTimes = kMinBytesToInsert + Rand(MaxBytesToInsert - kMinBytesToInsert + 1)
            bs = [Rand(256)] * repeatedTimes
            s = Rand(len(data) + 1)
            l = list(data)
            tmpl = l[0 : s] + bs + l[s :]
            return bytes(tmpl)
            
    def Mutate_ChangeByte(self, data):
        if len(data) > self.maxSize or len(data) == 0:
            return data
        else:
            b = Rand(256)
            s = Rand(len(data))
            l = list(data)
            l[s] = b
            return bytes(l)

    def Mutate_ChangeBit(self, data):
        if len(data) > self.maxSize or len(data) == 0:
            return data
        else:
            s = Rand(len(data))
            l = list(data)
            l[s] ^= 1 << Rand(8)
            return bytes(l)

    def Mutate_ShuffleBytes(self, data):
        if len(data) > self.maxSize or len(data) == 0:
            return data
        else:
            ShuffleAmount = Rand(min(8, len(data))) + 1
            ShuffleStart = Rand(len(data) - ShuffleAmount)
            l = list(data)
            tmpl = l[ShuffleStart : ShuffleStart + ShuffleAmount]
            shuffle(tmpl)
            l[ShuffleStart : ShuffleStart + ShuffleAmount] = tmpl
            return bytes(l)

    def Mutate_ChangeASCIIInteger(self, data):
        if len(data) > self.maxSize or len(data) == 0:
            return data
        else:
            B = Rand(len(data))
            while (B < len(data) and not isdigit(data[B])): B += 1
            if B == len(data):
                return data
            else:
                E = B + 1
                while (E < len(data) and isdigit(data[E])): E += 1
                l = list(data)
                digitl = l[B:E]
                val = int(bytes(digitl))

                sw = Rand(5)
                if sw == 0:  val += 1
                elif sw == 1: val -= 1
                elif sw == 2:  val //= 2
                elif sw == 3: val *= 2
                else: val = Rand(val*val)

                digitl = [0] * len(digitl)
                de = len(digitl) - 1
                for v in str(val)[::-1]:
                    if de < 0:
                        break
                    digitl[de] = ord(v)
                    de -= 1

                l[B:E] = digitl
                return bytes(l)

    def Mutate_ChangeBinaryInteger(self, data):
        nd = 2 ** (Rand(4))  # 1 2 4 8
        
        if nd == 1:
            fmt = 'B'
        elif nd == 2:
            fmt = 'H'
        elif nd == 4:
            fmt = 'I'
        else:
            fmt = 'Q'
        
        if len(data) < nd:
            return data
        else:
            val = []
            Off = Rand(len(data) - nd + 1)
            l = list(data)
            if Off < 64 and not Rand(4):
                size = len(data) % (1 << 8 * nd)
                val = list(struct.pack('<' + fmt, size)) # x86小端序
                if Rand(1):
                    val = list(struct.pack('>' + fmt, size))  # 转为大端序
            else:
                val = struct.unpack('<' + fmt, bytes(l[Off:Off + nd]))[0]
                Add = Rand(21) - 10
                if Rand(1):
                    bval = struct.pack('>' + fmt, val) # 大端序pack，小端序unpack来实现__builtin_bswap
                    val += struct.unpack('<' + fmt, bval)[0]
                    val += Add
                    val = val % (1 << 8 * nd)
                    bval = struct.pack('>' + fmt, val)
                    val += struct.unpack('<' + fmt, bval)[0]
                else:
                    val += Add
                if Add == 0 or Rand(0):
                    val = -val
                val = val % (1 << 8 * nd)
                val = list(struct.pack('<' + fmt, val))

            l[Off:Off + nd] = val

            return bytes(l)

    def Mutate_CopyPart(self, data):
        if len(data) > self.maxSize or len(data) == 0:
            return data
        else:
            ToBeg = Rand(len(data))
            FromBeg = Rand(len(data))
            CopySize = Rand(min(len(data) - FromBeg, self.maxSize - len(data)))
            l = list(data)
            tmpl = l[FromBeg : FromBeg + CopySize]
            if Rand(1): # 1
                l = l[0:ToBeg] + tmpl + l[ToBeg+CopySize:]
            else: # 0
                l = l[0:ToBeg] + tmpl + l[ToBeg:]
            return bytes(l)
    
    def Mutate_AddWordFromManualDictionary(self, data):
        return data

    def mutate(self, idx, data):
        if 0 <= idx < self.methodNum:
            mutatorFunc = self.funcMap[idx]
            return mutatorFunc(data)[:self.maxSize]

"""
加入位置和强度信息
    loc
    density
"""
class FuzzMutatorPlus():
    def __init__(self, maxSize, userDict=None):
        self.maxSize = maxSize
        self.userDict = userDict
        self.funcMap = {
            0: self.Mutate_EraseBytes,
            1: self.Mutate_InsertByte,
            2: self.Mutate_InsertRepeatedBytes,
            3: self.Mutate_ChangeByte,
            4: self.Mutate_ChangeBit,
            5: self.Mutate_ShuffleBytes,
            6: self.Mutate_ChangeASCIIInteger,
            7: self.Mutate_ChangeBinaryInteger,
            8: self.Mutate_CopyPart,
            # 9: self.Mutate_Random
            # 9: self.Mutate_AddWordFromManualDictionary
        }
        self.methodNum = len(self.funcMap)
    
    def Mutate_Random(self, data, loc, density):
        return self.funcMap[Rand(self.methodNum - 1)](data, loc, density)
    
    """
    density [0, len-loc]
    """
    def Mutate_EraseBytes(self, data, loc, density):
        if len(data) > 0:
            return data[0:loc] + data[loc+density//4:] # [0,64]
        else:
            return data
    
    """
    loc [0, len]
    density [0, 256]
    """
    def Mutate_InsertByte(self, data, loc, density):
        if len(data) >= self.maxSize:
            return data
        else:
            l = list(data)
            l.insert(loc, density)
            return bytes(l)
    
    """
    loc [0, len]
    density [0, 256]
    """
    def Mutate_InsertRepeatedBytes(self, data, loc, density):
        kMinBytesToInsert = 3
        if kMinBytesToInsert + len(data) >= self.maxSize:
            return data
        else:
            MaxBytesToInsert = min(self.maxSize - len(data), 128)
            repeatedTimes = kMinBytesToInsert + Rand(MaxBytesToInsert - kMinBytesToInsert + 1)
            bs = [density] * repeatedTimes
            l = list(data)
            tmpl = l[0 : loc] + bs + l[loc :]
            return bytes(tmpl)
    
    """
    loc [0, len]
    density [0, 256]
    """
    def Mutate_ChangeByte(self, data, loc, density):
        if len(data) > self.maxSize or len(data) == 0:
            return data
        else:
            l = list(data)
            l[loc] = density
            return bytes(l)
    
    """
    loc [0, len]
    density [0, 8]
    """
    def Mutate_ChangeBit(self, data, loc, density):
        if len(data) > self.maxSize or len(data) == 0:
            return data
        else:
            l = list(data)
            l[loc] ^= 1 << (density % 8)
            return bytes(l)
    
    """
    loc [0, len]
    density [0, 8]
    """
    def Mutate_ShuffleBytes(self, data, loc, density):
        if len(data) > self.maxSize or len(data) == 0:
            return data
        else:
            ShuffleAmount = density % 8
            ShuffleStart = loc
            l = list(data)
            tmpl = l[ShuffleStart : ShuffleStart + ShuffleAmount]
            shuffle(tmpl)
            l[ShuffleStart : ShuffleStart + ShuffleAmount] = tmpl
            return bytes(l)

    """
    loc [0, len]
    density [0, 5]
    """
    def Mutate_ChangeASCIIInteger(self, data, loc, density):
        if len(data) > self.maxSize or len(data) == 0:
            return data
        else:
            B = loc
            while (B < len(data) and not isdigit(data[B])): B += 1
            if B == len(data):
                return data
            else:
                E = B + 1
                while (E < len(data) and isdigit(data[E])): E += 1
                l = list(data)
                digitl = l[B:E]
                val = int(bytes(digitl))

                sw = density % 5
                if sw == 0:  val += 1
                elif sw == 1: val -= 1
                elif sw == 2:  val //= 2
                elif sw == 3: val *= 2
                else: val = Rand(val*val)

                digitl = [0] * len(digitl)
                de = len(digitl) - 1
                for v in str(val)[::-1]:
                    if de < 0:
                        break
                    digitl[de] = ord(v)
                    de -= 1

                l[B:E] = digitl
                return bytes(l)
    
    """
    loc [0, len]
    density [0, 3]
    """
    def Mutate_ChangeBinaryInteger(self, data, loc, density):
        nd = 2 ** (density % 4)  # 1 2 4 8
        
        if nd == 1: fmt = 'B'
        elif nd == 2: fmt = 'H'
        elif nd == 4: fmt = 'I'
        else: fmt = 'Q'
        
        if len(data) < nd:
            return data
        else:
            val = []
            Off = loc if loc < len(data) - nd else len(data) - nd  # 确保取到nd个
            l = list(data)
            if Off < 64 and not density % 4:
                size = len(data) % (1 << 8 * nd)
                val = list(struct.pack('<' + fmt, size)) # x86小端序
                if loc % 2:
                    val = list(struct.pack('>' + fmt, size))  # 转为大端序
            else:
                val = struct.unpack('<' + fmt, bytes(l[Off:Off + nd]))[0]
                Add = Rand(21) - 10
                if loc % 2:
                    bval = struct.pack('>' + fmt, val) # 大端序pack，小端序unpack来实现__builtin_bswap
                    val += struct.unpack('<' + fmt, bval)[0]
                    val += Add
                    val = val % (1 << 8 * nd)
                    bval = struct.pack('>' + fmt, val)
                    val += struct.unpack('<' + fmt, bval)[0]
                else:
                    val += Add
                if Add == 0:
                    val = -val
                val = val % (1 << 8 * nd)
                val = list(struct.pack('<' + fmt, val))

            l[Off:Off + nd] = val

            return bytes(l)

    """
    loc [0, len] ToBeg
    density [0, len] CopySize
    """
    def Mutate_CopyPart(self, data, loc, density):
        if len(data) > self.maxSize or len(data) == 0:
            return data
        else:
            ToBeg = loc
            FromBeg = Rand(len(data))
            CopySize = density
            l = list(data)
            tmpl = l[FromBeg : FromBeg + CopySize]
            if density % 2: # 1
                l = l[0:ToBeg] + tmpl + l[ToBeg+CopySize:]
            else: # 0
                l = l[0:ToBeg] + tmpl + l[ToBeg:]
            return bytes(l)
    
    def Mutate_AddWordFromManualDictionary(self, data, loc, density):
        return data

    def mutate(self, idx, data, loc, density):
        loc, density = int(loc), int(density)
        assert 0 <= idx < self.methodNum
        if len(data) > 0:
            loc %= len(data)
            assert 0 <= loc < len(data)
        assert 0 <= density <= 255
        mutatorFunc = self.funcMap[idx]
        return mutatorFunc(data, loc, density)[:self.maxSize]

if __name__ == "__main__":
    mutator = FuzzMutatorPlus(128)
    input_data = b''

    from tqdm import tqdm
    for i in tqdm(range(1024*1024*2)):
        action = Rand(mutator.methodNum)
        input_data = mutator.mutate(action, input_data, Rand(128), randint(1, 255))
    print('[{:>35}] {}'.format(mutator.funcMap[action].__func__.__name__, input_data))
        # if not i % 1024*512:
        #     print('[{:>35}] {}'.format(mutator.funcMap[action].__func__.__name__, input_data))