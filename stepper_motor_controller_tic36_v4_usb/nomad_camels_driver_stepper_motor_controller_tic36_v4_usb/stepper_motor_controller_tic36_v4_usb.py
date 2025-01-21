from .stepper_motor_controller_tic36_v4_usb_ophyd import (
    Stepper_Motor_Controller_Tic36_V4_Usb,
)

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="stepper_motor_controller_tic36_v4_usb",
            virtual=False,
            tags=[],
            directory="stepper_motor_controller_tic36_v4_usb",
            ophyd_device=Stepper_Motor_Controller_Tic36_V4_Usb,
            ophyd_class_name="Stepper_Motor_Controller_Tic36_V4_Usb",
            **kwargs,
        )
        self.config["max_speed"] = 1000
        self.config["max_accel"] = 10000
        self.config["step_mode_set"] = 1
        self.config["current_limit"] = 143
        self.config["energize"] = False
        self.settings["serial_num"] = ""


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        labels = {
            "serial_num": "Serial number of the controller (run 'ticcmd --list' to find)",
            "max_speed": "maximum speed of the motor in microsteps/s",
            "max_accel": "maximum acceleration and deceleration of the motor in microsteps/s^2",
            "step_mode_set": "Number of microsteps per step. Acceptable values: 1, 2, 4, 8, 16, 32, 64, 128, 256",
            "current_limit": "Current limit; will be rounded down to the nearest allowed value",
            "energize": "Energize motor coils",
        }
        super().__init__(
            parent,
            "stepper_motor_controller_tic36_v4_usb",
            data,
            settings_dict,
            config_dict,
            additional_info,
            labels=labels,
        )
        self.load_settings()
