from ophyd import Component as Cpt

import imageio.v3 as imageio
import numpy as np
import os
import matplotlib.pyplot as plt
import pco
import json
from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
from ophyd import Device


class Pco_camera(Device):
    number_of_images = 1
    exposure_time = 0.1
    get_frame = Cpt(
        Custom_Function_SignalRO,
        name="get_frame",
        metadata={
            "units": "A.U.",
            "description": "get a single image with current settings",
        },
    )
    get_x = Cpt(
        Custom_Function_SignalRO,
        name="get_x",
        metadata={"units": "A.U.", "description": "get x"},
    )
    get_y = Cpt(
        Custom_Function_SignalRO,
        name="get_y",
        metadata={"units": "A.U.", "description": "get y"},
    )
    set_number_of_images = Cpt(
        Custom_Function_Signal,
        name="set_number_of_images",
        metadata={
            "units": "",
            "description": "set number of images averaged per measurement",
        },
    )
    set_exposure_time = Cpt(
        Custom_Function_Signal,
        name="set_exposure_time",
        metadata={"units": "s", "description": "set exposure time (single image)"},
    )
    read_config = Cpt(
        Custom_Function_SignalRO,
        name="read_config",
        metadata={"units": "", "description": "return camera config string"},
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
        serial_num=87,
        interface="USB 2.0",
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
        self.serial_num = serial_num
        self.interface = interface
        self.get_frame.read_function = self.get_frame_read_function
        self.get_x.read_function = self.get_x_read_function
        self.get_y.read_function = self.get_y_read_function
        self.set_number_of_images.put_function = self.set_number_of_images_put_function
        self.set_exposure_time.put_function = self.set_exposure_time_put_function
        self.read_config.read_function = self.read_config_read_function

        if name == "test":
            return
        self.camera = pco.Camera(serial=self.serial_num, interface=self.interface)
        self.camera.auto_exposure_off()

    def finalize_steps(self):
        self.camera.close()
        
    def read_config_read_function(self):
        return str(self.camera.configuration)

    def set_number_of_images_put_function(self, value):
        self.number_of_images = int(value)

    def set_exposure_time_put_function(self, value):
        self.exposure_time = float(value)

    def get_x_read_function(self):
        config_str = self.camera.configuration
        return np.arange(config_str["roi"][3])

    def get_y_read_function(self):
        config_str = self.camera.configuration
        return np.arange(config_str["roi"][2])

    def get_frame_read_function(self):
        self.camera.exposure_time = self.exposure_time
        self.camera.record(number_of_images=self.number_of_images, mode="sequence")
        image = self.camera.image_average()

        return image
