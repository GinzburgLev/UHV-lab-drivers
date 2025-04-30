from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
from ophyd import Device
import json
import numpy as np
import pathlib


class Thermocouple_Calibration_Script(Device):
    Temperature = Cpt(
        Custom_Function_SignalRO,
        name="Temperature",
        metadata={"units": "C", "description": "Measured temperature"},
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
        Room_T=20,
        V_offset=0,
        Voltmeter_name="adc_x418",
        Voltmeter_channel_name="read_channel_1",
        Calibration_file_name="calibration_table_thermocouple_K.dat",
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs,
        )
        self.Voltmeter_name = Voltmeter_name
        self.Voltmeter_channel_name = Voltmeter_channel_name
        self.Calibration_file_name = Calibration_file_name
        self.Room_T = Room_T
        self.V_offset = V_offset
        self.Temperature.read_function = self.Temperature_read_function

    def Temperature_read_function(self):
        from nomad_camels.utility import device_handling

        device = device_handling.running_devices[self.Voltmeter_name]
        # output = device.read_current_output_actual.get()
        func_name = getattr(device, self.Voltmeter_channel_name)
        V_meas_no_offset = func_name.get()
        if type(V_meas_no_offset) == float:
            V_meas = V_meas_no_offset - self.V_offset
        else:
            V_meas_no_offset = func_name.get()
            if type(V_meas_no_offset) == float:
                V_meas = V_meas_no_offset - self.V_offset
            else:
                V_meas = self.V_offset
                print(f"failed to receive voltage")
        path_to_calibration = pathlib.Path(__file__).parent.resolve()
        with open(
            str(path_to_calibration) + "/" + self.Calibration_file_name, "r"
        ) as filehandle:
            data = json.load(filehandle)
        t_array = np.array(data.get("t, C", []))
        V_array = np.array(data.get("V, V", []))
        index = (np.abs(V_array - V_meas)).argmin()
        filehandle.close()
        return t_array[index] + self.Room_T
