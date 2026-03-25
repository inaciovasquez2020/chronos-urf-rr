import math

def ball_size_F2(R: int) -> int:
    # |B_R| = 1 + 4 * (3^R - 1)/2  for R>=0
    return 1 + 2 * (3**R - 1)

def approx_kappa(maxR: int = 20) -> float:
    vals = []
    for R in range(5, maxR + 1):
        vals.append((1.0 / R) * math.log(ball_size_F2(R)))
    return sum(vals) / len(vals)

if __name__ == "__main__":
    print("kappa(F2,S) exact =", math.log(3))
    print("kappa(F2,S) approx =", approx_kappa(25))
    # check the trivial upper bound numerically for a synthetic collision model
    # (here we just demonstrate the counting inequality form)
    for R in [5, 10, 15]:
        BR = ball_size_F2(R)
        col = 1 + R  # polynomial collision proxy
        code_lower = BR // col
        print(f"R={R} |B_R|={BR} Col~{col} lower(|Code|)={code_lower}")
