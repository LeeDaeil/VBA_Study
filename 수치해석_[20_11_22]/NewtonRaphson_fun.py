"""
Newton Raphson 법을 사용한 근 계산기 (by Daeil Lee)

Ref
    1. https://www.codesansar.com/numerical-methods/newton-raphson-method-python-program.htm
    2. https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.newton.html
"""
import matplotlib.pylab as plt
import argparse
from random import randint
from math import *
from sympy import *
import time


class NewtonRaphsonFun:
    def __init__(self, fun=object, der_fun=object, x_min=float, x_max=float, x_init=float, err=float):
        """
        Newton Raphson 법을 사용한 근 계산기

        :param fun: lambda 함수로 작성된 함수를 사용하거나 def 로 작성된 함수 사용
                    (e.x)
                        def fun(x):
                            y = x ** 2 + x
                            return y
        :param der_fun: lambda 함수로 작성된 함수를 사용하거나 def 로 작성된 함수 사용
        :param x_min: x의 최소 범위
        :param x_max: x의 최대 범위
        :param err: error 범위
        """
        # init part
        self._get_fun = sympify(fun)
        self._get_der_fun = diff(fun, 'x')
        if x_init is not None:
            self._get_x_0 = x_init
        else:
            self._get_x_0 = randint(x_min, x_max)
        self._get_error = abs(err)

        self._x_0 = self._get_x_0  # _step 진행 시 업데이트

        self._info = {'x_start_ran_x0': self._get_x_0, 'x_ran_x0_list': [],
                      'iter': 0, 'iter_list': [],
                      'root': 0, }

        # assert part
        if x_min != None or x_max != None:
            assert not x_min >= x_max, 'x_min 값은 x_max 보다 커야합니다.'
        # assert fun(x_min) * fun(x_max) < 0, f'[{x_min}~{x_max}] 구간 사이에 근이 없습니다.'

        self._run()

    def _log(self):
        self._info['x_ran_x0_list'].append(self._x_0)
        self._info['iter_list'].append(self._info['iter'])
        self._info['root'] = self._x_0
        self._info['iter'] += 1

    def _run(self):
        print(f"Start {self._info['x_start_ran_x0']} ====== ")

        while True:
            print(f"Iter: {self._info['iter']}|"
                  f"Root: {self._x_0}|")

            # 1. 미분 값이 0 인지 확인 후 종료
            if self._get_der_fun.subs('x', self._x_0) == 0:
                print('Divide by zero error!')
                break

            # 2. 계산 및 업데이트
            new_x_0 = self._x_0 - (self._get_fun.subs('x', self._x_0) / self._get_der_fun.subs('x', self._x_0))

            # -. logger
            self._log()
            self._x_0 = new_x_0
            # 3. err 보다 작으면 종료
            if abs(self._get_fun.subs('x', new_x_0)) < self._get_error: break

        print('Done!')

    def get_info(self):
        print(f"Iter: {self._info['iter']}|"
              f"Root: {self._info['root']}|")
        return 0

    def plot(self):
        plt.plot(self._info['x_ran_x0_list'], label='x_0')
        plt.xlabel('Iter')
        plt.ylabel('X value')
        plt.legend()
        plt.grid()
        plt.show()


parser = argparse.ArgumentParser(description='Newton Raphson법 사용한 근 계산기 (by Daeil Lee)')
parser.add_argument('--fun', type=str, required=True, help="함수식 f(x)")
parser.add_argument('--xmin', type=float, required=False, help="x min")
parser.add_argument('--xmax', type=float, required=False, help="x max")
parser.add_argument('--xinit', type=float, required=False, help="x init")
parser.add_argument('--err', type=float, required=True, help="error")
args = parser.parse_args()

out = NewtonRaphsonFun(fun=args.fun, x_min=args.xmin, x_max=args.xmax,
                       x_init=args.xinit, err=args.err)
out.get_info()
out.plot()
