from simulator import Simulator

from tango import AttrWriteType
from tango.server import Device, attribute, command, run


class PaintTank(Device):
    """
    Tango device server implementation representing a single paint tank
    """
    def init_device(self):
        super().init_device()
        print("Initializing %s for %s" % (self.__class__.__name__, self.get_name()))
        # extract the tank name from the full device name, e.g. "epfl/station1/cyan" -> "cyan"
        tank_name = self.get_name().split('/')[-1]
        # get a reference to the simulated tank
        self.tank = simulator.get_paint_tank_by_name(tank_name)
        
        if self.tank.name == "cyan":
            self.nb = 0
        elif self.tank.name == "magenta":
            self.nb = 1
        elif self.tank.name == "yellow":
            self.nb = 2
        elif self.tank.name == "black":
            self.nb = 3
        elif self.tank.name == "white":
            self.nb = 4
        else:
            self.nb = 5
       
        if not self.tank:
            raise Exception(
                "Error: Can't find matching paint tank in the simulator with given name = %s" % self.get_name())

    @attribute(dtype=float)
    def level(self):
        """
        get level attribute
        range: 0 to 1
        """
        

        level = simulator.tanks[self.nb].get_level()
        return level

    @attribute(dtype=float)
    def flow(self):
        """
        get flow attribute
        """
        # TODO: return flow of simulated tank
        return simulator.tanks[self.nb].get_outflow()

    valve = attribute(label="valve", dtype=float,
                      access=AttrWriteType.READ_WRITE,
                      min_value=0.0, max_value=1.0,
                      fget="get_valve", fset="set_valve")

    def set_valve(self, ratio):
        """
        set valve attribute
        :param ratio: 0 to 1
        """
        
        simulator.tanks[self.nb].set_valve(ratio)

    def get_valve(self):
        """
        get valve attribute (range: 0 to 1)
        """
        # TODO: get valve of simulated tank
        return simulator.tanks[self.nb].get_valve()

    @attribute(dtype=str)
    def color(self):
        """
        get color attribute (hex string)
        """
        # TODO: get color of simulated tank
        color = simulator.tanks[self.nb].get_color_rgb()
        return color  

    @command(dtype_out=float)
    def Fill(self):
        """
        command to fill up the tank with paint
        """
        # TODO: fill simulated tank and return new level
        return simulator.tanks[self.nb].fill()

    @command(dtype_out=float)
    def Flush(self):
        """
        command to flush all paint
        """
        # TODO: flush simulated tank and return new level
        return simulator.tanks[5].flush()


if __name__ == "__main__":
    # start the simulator as a background thread
    simulator = Simulator()
    simulator.start()

    # start the Tango device server (blocking call)
    run((PaintTank,))
