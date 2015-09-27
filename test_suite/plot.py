from matplotlib import pyplot
from math import pi
from numpy import sin, cos, tan, arctan, arccos, arcsin, sinh, cosh, tanh, sqrt

x = [float(i) for i in open("x")]
sin_x = [float(i) for i in open("sin_x")]
sin_x_error = sin(x) - sin_x
cos_x = [float(i) for i in open("cos_x")]
cos_x_error = cos(x) - cos_x
tan_x = [float(i) for i in open("tan_x")]
tan_x_error = tan(x) - tan_x

x_2 = [float(i) for i in open("x_2")]
atan_x = [float(i) for i in open("atan_x")]
atan_x_error = arctan(x_2) - atan_x
x_3 = [float(i) for i in open("x_3")]
asin_x = [float(i) for i in open("asin_x")]
asin_x_error = arcsin(x_3) - asin_x
acos_x = [float(i) for i in open("acos_x")]
acos_x_error = arccos(x_3) - acos_x

x_4 = [float(i) for i in open("x_4")]
sinh_x = [float(i) for i in open("sinh_x")]
sinh_x_error = sinh(x_4) - sinh_x
cosh_x = [float(i) for i in open("cosh_x")]
cosh_x_error = cosh(x_4) - cosh_x
tanh_x = [float(i) for i in open("tanh_x")]
tanh_x_error = tanh(x_4) - tanh_x

x_5 = [float(i) for i in open("x_5")]
sqrt_x = [float(i) for i in open("sqrt_x")]
sqrt_x_error = sqrt(x_5) - sqrt_x

print "cosine max error", max(cos_x_error)
print "sine max error", max(sin_x_error)
print "tangent max error", max(tan_x_error)

pyplot.xticks(
    [-2.0*pi, -pi, 0, pi,  2.0*pi],
    [r'$-2\pi$', r"$-\pi$", r'$0$', r'$\pi$', r'$2\pi$'])


pyplot.figure(1)

ax = pyplot.subplot(231)
pyplot.plot(x, cos_x)
ax2 = ax.twinx()
ax2.plot(x, cos_x_error, "0.75")
pyplot.ylim(-5.5, 5.5)
ax2.set_ylim(-2e-12, 2e-12)
pyplot.xlim(-2.2 * pi, 2.2 * pi)
pyplot.title("cos(x)")
pyplot.xlabel("x (radians)")

ax = pyplot.subplot(232)
pyplot.plot(x, sin_x)
ax2 = ax.twinx()
ax2.plot(x, sin_x_error, "0.75")
pyplot.ylim(-5.5, 5.5)
ax2.set_ylim(-2e-12, 2e-12)
pyplot.xlim(-2.2 * pi, 2.2 * pi)
pyplot.title("sin(x)")
pyplot.xlabel("x (radians)")

ax = pyplot.subplot(233)
pyplot.plot(x, tan_x)
ax2 = ax.twinx()
ax2.plot(x, tan_x_error, "0.75")
ax.set_ylim(-5.5, 5.5)
ax2.set_ylim(-2e-11, 2e-11)
pyplot.xlim(-2.2 * pi, 2.2 * pi)
pyplot.title("tan(x)")
pyplot.xlabel("x (radians)")

ax = pyplot.subplot(234)
pyplot.plot(x_2, atan_x)
ax2 = ax.twinx()
ax2.plot(x_2, atan_x_error, "0.75")
ax.set_xlim(-5.5, 5.5)
ax.set_ylim(-2, 2)
ax2.set_ylim(-2e-13, 2e-13)
pyplot.title("atan(x)")
pyplot.xlabel("x (radians)")

ax = pyplot.subplot(235)
pyplot.plot(x_3, asin_x)
ax2 = ax.twinx()
ax2.plot(x_3, asin_x_error, "0.75")
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-2, 2)
ax2.set_ylim(-2e-13, 2e-13)
pyplot.title("asin(x)")
pyplot.xlabel("x (radians)")

ax = pyplot.subplot(236)
pyplot.plot(x_3, acos_x)
ax2 = ax.twinx()
ax2.plot(x_3, acos_x_error, "0.75")
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-0.5, 3.5)
ax2.set_ylim(-2e-13, 2e-13)
pyplot.title("acos(x)")
pyplot.xlabel("x (radians)")

pyplot.figure(2)

ax = pyplot.subplot(231)
pyplot.plot(x_4, cosh_x)
ax2 = ax.twinx()
ax2.plot(x_4, cosh_x_error, "0.75")
ax2.set_ylim(-4e-6, 4e-6)
pyplot.xlim(-15, 15)
pyplot.title("cosh(x)")
pyplot.xlabel("x (radians)")

ax = pyplot.subplot(232)
pyplot.plot(x_4, sinh_x)
ax2 = ax.twinx()
ax2.plot(x_4, sinh_x_error, "0.75")
ax2.set_ylim(-4e-6, 4e-6)
pyplot.xlim(-15, 15)
pyplot.title("sinh(x)")
pyplot.xlabel("x (radians)")

ax = pyplot.subplot(233)
pyplot.plot(x_4, tanh_x)
ax2 = ax.twinx()
ax2.plot(x_4, tanh_x_error, "0.75")
ax2.set_ylim(-4e-6, 4e-6)
pyplot.xlim(-15, 15)
pyplot.title("tanh(x)")
pyplot.xlabel("x (radians)")

pyplot.figure(3)

pyplot.plot(x_5, sqrt_x)
ax2 = ax.twinx()
ax2.plot(x_5, sqrt_x_error, "0.75")
ax2.set_ylim(-4e-6, 4e-6)
pyplot.xlim(0, 10)
pyplot.title("sqrt(x)")
pyplot.xlabel("x")

pyplot.show()
