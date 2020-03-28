import argparse
import numpy as np

from math import sqrt
from scipy.stats import norm

def make_bounce(minv, maxv):
    def bounce(oldval, delta):
        val = oldval + delta
        while val < minv or val > maxv:
            if val < minv:
                diff = minv - val
                val = minv + diff
            if val > maxv:
                diff = val - maxv
                val = maxv - diff
        return val
    return bounce

def make_ubounce(minv, maxv):
    bounce = make_bounce(minv, maxv)
    return np.frompyfunc(bounce, 2, 1)

def brownian(numx, nsteps, dt, delta, xmin, xmax, out=None):
    inits = np.random.randint(xmin, xmax, (numx, 1))
    r = norm.rvs(size=(numx,) + (nsteps,), scale=delta*sqrt(dt))
    v = np.concatenate((inits, r), axis=1)
    bounce = make_ubounce(xmin, xmax)
    if out is None:
        out = np.empty(v.shape)
    bounce.accumulate(v, axis=1, out=out, dtype=np.object).astype(np.int)
    return out

def get_args():
    parser = argparse.ArgumentParser(
        description="Run simulation",
    )
    parser.add_argument(
        '--speed',
        default=2,
        type=int,
        help='pos at time t is normal with mean x0, variance is delta**2*t',
    )
    parser.add_argument(
        '--num_steps',
        default=10,
        type=int,
        help='number of steps to take',
    )
    parser.add_argument(
        '--total_time',
        default=10,
        type=int,
        help='number of time units to simulate',
    )
    parser.add_argument(
        '--xmin',
        default=0,
        type=int,
        help='minimum value of x',
    )
    parser.add_argument(
        '--xmax',
        default=100,
        type=int,
        help='max value of x',
    )
    parser.add_argument(
        '--numx',
        default=1,
        type=int,
        help='number of x to simulate',
    )
    return parser.parse_args()

def main():
    args = get_args()
    dt = args.total_time / args.num_steps
    motion = brownian(
        args.numx,
        args.num_steps,
        dt,
        args.speed,
        args.xmin,
        args.xmax,
    )
    print(motion)

if __name__ == '__main__':
    main()
