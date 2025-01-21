from .thermocouple_calibration_script_ophyd import Thermocouple_Calibration_Script

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="thermocouple_calibration_script",
            virtual=False,
            tags=[],
            directory="thermocouple_calibration_script",
            ophyd_device=Thermocouple_Calibration_Script,
            ophyd_class_name="Thermocouple_Calibration_Script",
            **kwargs,
        )
        self.settings["Room_T"] = 23
        self.settings["V_offset"] = -0.0005
        self.settings["Voltmeter_name"] = "adc_x418"
        self.settings["Voltmeter_channel_name"] = "read_channel_1"
        self.settings["Calibration_file_name"] = "calibration_table_thermocouple_K.dat"


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
            "Room_T": "Environment temperature (C)",
            "V_offset": "Offset of the voltmeter (value measured at T=room_T) (V)",
            "Voltmeter_name": "Driver name of the voltmeter (should be accessible in current CAMELS session)",
            "Voltmeter_channel_name": "Channel name used to read out the voltage",
            "Calibration_file_name": "Name of the file containing calibration data. Should be in the same folder as driver",
        }
        super().__init__(
            parent,
            "thermocouple_calibration_script",
            data,
            settings_dict,
            config_dict,
            additional_info,
            labels=labels,
        )
        self.load_settings()
