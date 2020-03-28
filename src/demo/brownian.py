import argparse
import numpy as np

from math import sqrt
from scipy.stats import norm

from demo.shared_params import add_brownian_args

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

def brownian(numx, nsteps, dt, delta, xmin, xmax, dec, out=None):
    inits = np.random.randint(xmin, xmax, (numx, 1))
    r = norm.rvs(size=(numx,) + (nsteps,), scale=delta*sqrt(dt))
    v = np.concatenate((inits, r), axis=1)
    bounce = make_ubounce(xmin, xmax)
    if out is None:
        out = np.empty(v.shape)
    bounce.accumulate(v, axis=1, out=out, dtype=np.object).astype(np.int)
    if dec != None:
        out = np.round(out, dec)
    if dec == 0:
        out = out.astype(int)

    return out

def get_args():
    parser = argparse.ArgumentParser(
        description="Run simulation",
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
    parser = add_brownian_args(parser)
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
        args.round,
    )
    print(motion)

if __name__ == '__main__':
    main()
