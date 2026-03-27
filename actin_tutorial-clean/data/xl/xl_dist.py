import numpy


inp = numpy.genfromtxt("lys_ca_distances.dat", delimiter=" ", dtype="S1,i8,f8,f8,f8")




for i,g in enumerate(inp[:-1]):
    for h in inp[i+1:]:
        d = ((g[2]-h[2])**2+(g[3]-h[3])**2+(g[4]-h[4])**2)**0.5
        if d < 25 and d > 15 and g[0] != h[0]:
            print g[0], ",",int(g[1]), ",",h[0], ",",int(h[1])