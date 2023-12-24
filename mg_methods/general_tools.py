import numpy as np


def wrapper_fn(func):

    def inner1(*x, **a):
        c = func(*x, **a)
        return c

    return inner1


def tealPythonWrapper(functionName, *fnVaraibles, **functionParameters):
    '''functionParameters is a dictionary of the parameters to be passed to the function'''

    function_to_be_called = wrapper_fn(functionName)
    return function_to_be_called(*fnVaraibles, **functionParameters)


def get_keys(dictionary):
    result = []
    for key, value in dictionary.items():
        if type(value) is dict:
            new_keys = get_keys(value)
            result.append(key)
            for innerkey in new_keys:
                result.append(f'{key}/{innerkey}')
        else:
            result.append(key)
    return result


def divide_sections(numSecns, tmp):
    total = sum([tmp[xx] for xx in [*tmp]])
    if numSecns > 1:
        possibleSecns = [xx for xx in algorithm_u([*tmp], numSecns)]
        possibleSecnNumbers = [
            [max(sum([tmp[xx] for xx in zz]), 1) for zz in yy] for yy in possibleSecns]
        entropyOfPartition = [-sum([(zz/total)*np.log((zz/total))
                                   for zz in xx]) for xx in possibleSecnNumbers]
        optimalPartition = possibleSecns[np.where(
            entropyOfPartition == np.amax(entropyOfPartition))[0][0]]
        # print(optimalPartition)
    else:
        optimalPartition = [[*tmp]]
    return optimalPartition  # New 01/09/2022


def algorithm_u(ns, m):
    def visit(n, a):
        ps = [[] for i in range(m)]
        for j in range(n):
            ps[a[j + 1]].append(ns[j])
        return ps

    def f(mu, nu, sigma, n, a):
        if mu == 2:
            yield visit(n, a)
        else:
            for v in f(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v
        if nu == mu + 1:
            a[mu] = mu - 1
            yield visit(n, a)
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                yield visit(n, a)
        elif nu > mu + 1:
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = mu - 1
            else:
                a[mu] = mu - 1
            if (a[nu] + sigma) % 2 == 1:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v

    def b(mu, nu, sigma, n, a):
        if nu == mu + 1:
            while a[nu] < mu - 1:
                yield visit(n, a)
                a[nu] = a[nu] + 1
            yield visit(n, a)
            a[mu] = 0
        elif nu > mu + 1:
            if (a[nu] + sigma) % 2 == 1:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] < mu - 1:
                a[nu] = a[nu] + 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = 0
            else:
                a[mu] = 0
        if mu == 2:
            yield visit(n, a)
        else:
            for v in b(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v

    n = len(ns)
    a = [0] * (n + 1)
    for j in range(1, m + 1):
        a[n - m + j] = j - 1
    return f(m, n, 0, n, a)
