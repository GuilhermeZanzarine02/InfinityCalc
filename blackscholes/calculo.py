import math as m
import scipy.stats as stats


def calculos_intermediarios(s, x, r, t, sigma):
    d1 = (m.log(s/x) + (r + (sigma**2) / 2) * t) /(sigma * m.sqrt(t))
    d2 = d1 - sigma * m.sqrt(t)
    return d1, d2


def calculo_nd1_nd2(d1, d2):
    nd1 = stats.norm.cdf(d1)
    nd2 = stats.norm.cdf(d2)
    nd1n = stats.norm.cdf(-d1)
    nd2n = stats.norm.cdf(-d2)

    return nd1, nd2, nd1n, nd2n


def calculo_blaack_sholes(s, x, r, t, nd1, nd2, nd1n, nd2n):
    call = s * nd1 - x * m.exp(-r * t) * nd2
    put = x * m.exp(-r * t) * nd2n - s * nd1n

    call = "{:.2f}".format(call)
    put = "{:.2f}".format(put)

    return call, put