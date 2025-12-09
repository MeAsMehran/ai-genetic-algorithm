# model.py
import math
from config import ALPHA

# --------------------------
# Q و F و Cost
# --------------------------

def Q_linear(p):
    p1,p2,p3,p4,p5 = p
    return 2.5*p1 + 1.8*p2 + 1.2*p3 + 1.5*p4 + 1.0*p5 - 700


def F_p(p):
    p1,p2,p3,p4,p5 = p
    q_lin = Q_linear(p)

    nonlinear = (
        2.5*p5
        - 0.18*(p4**2)
        - 2*(p2 + p1)
        + 5*math.exp(-10*p5*(p4**2))
        + 2.5*math.sin(6*math.pi*p3)
        - 3*(p2*p1)
    )

    term = 2.5*(p5 + p4 + 1.5*p3 + 1.2*p2 + 1.8*p1)
    return q_lin + nonlinear + term


def multiplier_M(p):
    p1,p2,p3,p4,p5 = p
    return (p1/50)*(p2/50)*(p3/50)*(p4/50)*(p5/50)


def Q_raw(p):
    return F_p(p) * multiplier_M(p)


def Q_final(p):
    qraw = Q_raw(p)
    return 20 * (1 / (1 + math.exp(-0.8*(qraw - 5))))


def C_norm(p):
    p1,p2,p3,p4,p5 = p
    return 0.9*p1 + 1.1*p2 + 0.8*p3 + 0.6*p4 + 1.4*p5


# --------------------------
# بهبود مهم در نرمال‌سازی fitness
# --------------------------
def fitness_of(p, alpha=ALPHA):
    q = Q_final(p)
    q_norm = q / 20.0

    cost = C_norm(p)
    
    # مقیاس‌بندی بهتر
    cost_scaled = (cost - 60) / 80  # تبدیل به 0..1

    return alpha*q_norm + (1-alpha)*(1 - cost_scaled)
