import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import sympy as sym
from scipy.integrate import quad


class CycloidalCurves:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-6, 6)

        self.r = 1.
        self.arc_length = 0

        self.centre, = self.ax.plot([], [], 'ko', ms=2)
        self.traced, = self.ax.plot([], [], 'r')
        self.curve, = self.ax.plot([], [], 'm')
        self.radius, = self.ax.plot([], [], 'g')
        self.circle, = self.ax.plot([], [], 'c')

        self.circle_pts = np.linspace(0, 2 * np.pi, 80)
        self.traced_x, self.traced_y = [], []
        self.curve_x, self.curve_y = [], []

        self.anim = None
        self.func = 'sin(x)'

    def data_init(self):
        self.centre.set_data([], [])
        self.traced.set_data([], [])
        self.curve.set_data([], [])
        self.radius.set_data([], [])
        self.circle.set_data([], [])
        curve_pts = np.linspace(-100, 100, 30000)
        self.curve.set_data(curve_pts, self.fun(curve_pts))
        return self.centre, self.traced, self.curve, self.radius, self.circle

    def get_functions(self):
        x = sym.Symbol('x')
        derivative = sym.diff(self.func, x)
        self.fun = sym.lambdify(x, self.func)
        self.der = sym.lambdify(x, derivative)
        self.integ = sym.lambdify(x, sym.sqrt(1 + derivative**2))

    def draw(self, t, speed):
        t *= speed
        self.arc_length += quad(self.integ, t - speed, t, limit=100)[0]

        try:
            x_circle = t - ((self.r * self.der(t)) / np.sqrt(1 + self.der(t)**2))
            y_circle = self.fun(t) + self.r / np.sqrt(1 + self.der(t)**2)
            angle = np.arctan(self.der(t)) - (1 / self.r) * self.arc_length

            x = x_circle + self.r * np.sin(angle)
            y = y_circle - self.r * np.cos(angle)

            self.traced_x.append(x)
            self.traced_y.append(y)
            self.curve_x.append(t)
            self.curve_y.append(self.fun(t))

            self.circle.set_data(
                x_circle + self.r * np.cos(self.circle_pts),
                y_circle + self.r * np.sin(self.circle_pts)
            )
            self.traced.set_data(self.traced_x, self.traced_y)
            self.centre.set_data([x_circle], [y_circle])
            self.radius.set_data([x_circle, x], [y_circle, y])
            self.curve.set_data(self.curve_x, self.curve_y)

            self.ax.set_xlim(x_circle - 10, x_circle + 10)
        except Exception as e:
            print(f"Error during draw: {e}")

        return self.circle, self.traced, self.centre, self.radius, self.curve

    def start_animation(self, speed=0.1):
        if not self.anim:
            self.anim = animation.FuncAnimation(self.fig, func=self.draw, init_func=self.data_init, 
                                                fargs=(speed,), interval=20, blit=True, 
                                                save_count=200)
        else:
            self.anim.event_source.start()

    def stop_animation(self):
        self.anim.event_source.stop()



if __name__ == '__main__':
    rolling_circle = CycloidalCurves()
    rolling_circle.get_functions()
    rolling_circle.start_animation()
    plt.show()
