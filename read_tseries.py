from typing import *
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore

T = TypeVar('T')
U = TypeVar('U')

def read_csv_header(fn: str) -> List[Tuple[str, List[float]]]:
    tseries = list()
    with open(fn, 'r') as fin:
        fin.readline()
        for ln in fin:
            elems = [elem.strip() for elem in ln.strip().split(",")]
            country_name = elems[1]
            ts = [float(elem.strip()) for elem in elems[5:]]
            tseries.append((country_name, ts))

    return tseries

def get_a(kvs: List[Tuple[T, U]], ks: T) -> List[U]:
    return [v for k, v in kvs if k == ks]

def get_max(ns, f):
    sns = sorted([(i, f(n)) for i, n in enumerate(ns)],
                 key=lambda x: x[1],
                 reverse=True)
    (i, _) = sns[0]

    return ns[i]

def get_ds(ts: List[float]) -> List[float]:
    return [n2-n1 for n1, n2 in zip(ts, ts[1:])]


def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / N

def calc_ln(ln: Tuple[float, float], x: float) -> float:
    a, b = ln

    return a*x + b
