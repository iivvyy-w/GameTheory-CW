import numpy as np

simulations = 10000
max_iters = 1000

N = 0
for i in range(simulations):
    x = [0, 0, 0, 0]
    for j in range(max_iters):
        if x >= [3, 3, 3, 3]:
            N += j
            break

        dx = np.random.choice(5, p=[0.7, 0.075, 0.075, 0.075, 0.075])
        if dx == 1:
            x[0] += 1
        elif dx == 2:
            x[1] += 1
        elif dx == 3:
            x[2] += 1
        elif dx == 4:
            x[3] += 1

print(N/simulations)
