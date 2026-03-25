import numpy as np

def lambda_c(Delta):
    return ((Delta - 1)**(Delta - 1)) / ((Delta - 2)**Delta)

def scan():
    for Delta in [10,12,16,20,30]:
        print("Delta =",Delta,"lambda_c =",lambda_c(Delta))

if __name__ == "__main__":
    scan()
