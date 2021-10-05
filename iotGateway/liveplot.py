import iotGateway as iot
from matplotlib import pyplot as plt
from matplotlib import animation as anim

# Note that plt.show() is a blocking function and therefore stops the thread. This must be in a separate thread
# TODO: Run in its own program (?)
def animation(x_val, y_val):

    def animate(i):
        # Note that a function call must be done here to update the x and y values
        iot.x_vals.append(x_val)
        iot.y_vals.append(y_val)
        plt.cla()
        plt.plot(iot.x_vals, iot.y_vals)
        # plt.plot(iot.x_vals, iot.y2_vals, label='motor1'
        # plt.legend(loc='upper left')
        # plt.tight_layout()

    ani = anim.FuncAnimation(plt.gcf(), animate, interval=1000)
    plt.tight_layout()
    plt.show()