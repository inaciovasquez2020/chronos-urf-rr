import numpy as np

def activity_to_lambda(rho):
    return rho / (1 - rho)

def lambda_to_activity(lam):
    return lam / (1 + lam)

def demo():
    rhos = [0.3608134472742677,
            0.285311670611,
            0.20105751706384203,
            0.15519163765696303,
            0.09881002264003105]

    for rho in rhos:
        lam = activity_to_lambda(rho)
        print("rho =", rho, "lambda =", lam)

if __name__ == "__main__":
    demo()
