from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
from nomad_camels.bluesky_handling.visa_signal import (
    VISA_Signal,
    VISA_Signal_RO,
    VISA_Device,
)
import time


class Leybold_Combivac_It23(VISA_Device):
    number_of_repeats = 5
    time_delay = 0.1
    read_pressure_S1 = Cpt(
        Custom_Function_SignalRO,
        name="read_pressure_S1",
        # query="MES 1",
        # parse_return_type="float",
        metadata={"units": "mbar", "description": "Read pressure channel S1"},
    )
    read_pressure_S2 = Cpt(
        Custom_Function_SignalRO,
        name="read_pressure_S2",
        # query="MES 2",
        # parse_return_type="float",
        metadata={"units": "mbar", "description": "Read pressure channel S2"},
    )
    read_pressure_ITR = Cpt(
        Custom_Function_SignalRO,
        name="read_pressure_ITR",
        # query="MES 3",
        # parse_return_type="float",
        metadata={"units": "mbar", "description": "Read pressure channel ITR"},
    )

    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        resource_name="",
        write_termination="\r",
        read_termination="\r",
        baud_rate=9600,
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            resource_name=resource_name,
            baud_rate=baud_rate,
            read_termination=read_termination,
            write_termination=write_termination,
            **kwargs,
        )
        self.read_pressure_S1.read_function = lambda: self.read_pressure_func(1)
        self.read_pressure_S2.read_function = lambda: self.read_pressure_func(2)
        self.read_pressure_ITR.read_function = lambda: self.read_pressure_func(3)

    def read_pressure_func(self, channel_num):
        data = float("NaN")
        for i in range(self.number_of_repeats):
            reply = self.visa_instrument.query("MES " + str(channel_num))
            message = reply.split(":")[2]
            if message == "NO SENSOR":
                print("Attempting to connect to the sensor, iteration " + str(i) + " failed.")
            else:
                try:
                    data = float(message.replace(" ", ""))
                except:
                    print("ERROR: " + reply)
                break
            time.sleep(self.time_delay)
        if message == "NO SENSOR":
            print("no pressure sensor connected")
        return data
