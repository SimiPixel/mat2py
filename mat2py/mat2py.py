from typing import Iterable
from scipy.io import loadmat
from pathlib import Path
import numpy as np 
from pympler.asizeof import asizeof 

def load(mat):
    path = Path(mat)
    mat = loadmat(mat)
    return matlabFile(mat)

class matlabFile(object):
    def __init__(self, data):
        self.__attr = []

        if isinstance(data, dict):
            self._process_dict(data)

        elif isinstance(data, np.ndarray):
            if not isinstance(data.dtype.names, Iterable):
                self._process_cell(data)
            else:
                self._process_array(data)

        else:
            raise Exception()

    def _process_dict(self, data):

        found_field = False
        for key in data.keys():
            if key[:2] != "__":
                found_field = True
                self.__setattr(key, matlabFile(data[key]))
        if not found_field:
            raise Exception()

    def _process_cell(self, arr):
        if not hasattr(self, "cell"):
            self.cell = []

        self.__attr.append("cell")

        for i, cell in enumerate(arr):
            self.cell.append(matlabFile(cell))

    def _process_array(self, arr):

        for i, field in enumerate(arr.dtype.names):
            deeper_arr = arr[0,0][i]

            if deeper_arr.dtype.names is None:
                # convert to float
                try:
                    deeper_arr = deeper_arr.astype(float)
                except:
                    raise ValueError(f"Currently only numeric arrays for values are allowed, can not convert type {arr.dtype} to type float")
            else:
                deeper_arr = matlabFile(deeper_arr)

            self.__setattr(field, deeper_arr)

    def __setattr(self, attr, value):
        self.__attr.append(attr)
        setattr(self, attr, value)

    def __iter__(self):
        for attr in self.__attr:
            if attr[:1] != "_":
                yield attr, getattr(self, attr)

    def __repr__(self) -> str:
        s=""
        for attr, _ in self.__iter__():
            s += attr + "; "
        return s

    def __len__(self):
        return len([_ for _ in self.__iter__()])

    def __getitem__(self, attr: str) -> object:
        return getattr(self, attr)

    def keys(self):
        return [item[0] for item in self.__iter__()]

    def values(self):
        return [item[1] for item in self.__iter__()]

    def items(self):
        return [item for item in self.__iter__()]

    def sizeInKiloBytes(self):
        return asizeof(self)/1024

    def sizeInMegaBytes(self):
        return asizeof(self)/1024/1024

    def pprint(self, lvl=0, return_str=False):
        s=""
        padding = lambda key, lvl: lvl*"--"+key+"\n"

        for key in self.keys():
            s += padding(key, lvl)
            if isinstance(self[key], np.ndarray):
                s += padding("array",lvl+1)
            elif isinstance(self[key], list):
                for cell in self[key]:
                    s += cell.pprint(lvl=lvl+1, return_str=True)
            else:
                s += self[key].pprint(lvl=lvl+1, return_str=True)

        if return_str:
            return s
        else:
            print(s)

    

            