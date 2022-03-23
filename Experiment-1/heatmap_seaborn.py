import torch
import seaborn as sns
import matplotlib.pylab as plt

a = torch.tensor([[-0.1124,  0.2930,  0.1379,  0.0444, -0.2036, -0.0514, -0.2497, -0.2494, -0.3150, -0.2250],
[-0.0283, -0.2422,  0.2848, -0.2104, -0.0912, -0.1891, -0.2807, -0.1128, -0.1197, -0.1885],
[-0.0331,  0.0915, -0.0272,  0.2902, -0.0951,  0.0071,  0.0850,  0.2515, -0.2799, -0.2824],
[-0.3056, -0.0832, -0.0684,  0.2448,  0.1002, -0.2027,  0.1688,  0.2561, 0.1393,  0.2952],
[-0.0486, -0.2082,  0.2176,  0.2986,  0.0336,  0.2487,  0.1141,  0.1112, -0.0954,  0.2644],
[-0.0049, -0.0755,  0.2186,  0.1433, -0.1790, -0.0525,  0.0867,  0.0394, 0.1172,  0.2695],
[ 0.0757,  0.0448,  0.1376,  0.2723, -0.1225,  0.2373,  0.2188, -0.2446, -0.2251,  0.1956],
[ 0.1085, -0.2348,  0.1529, -0.1381, -0.0666, -0.3256,  0.1151, -0.0858,-0.2615,  0.0222],
[ 0.1697,  0.1872, -0.1706,  0.2136,  0.0942,  0.1336, -0.1187, -0.0636, -0.3050,  0.0992],
[ 0.2573, -0.3054, -0.2908,  0.0974,  0.0934,  0.1321, -0.1117, -0.2675, 0.1868,  0.1718]], dtype=torch.float64)

#a = torch.mm(a.T, a)
ax = sns.heatmap(a, linewidth=0.5)
plt.savefig("weights.png")