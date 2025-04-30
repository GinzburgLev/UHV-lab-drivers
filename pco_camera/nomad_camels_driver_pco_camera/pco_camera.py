from .pco_camera_ophyd import Pco_camera

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="pco_camera",
            virtual=False,
            tags=[],
            directory="pco_camera",
            ophyd_device=Pco_camera,
            ophyd_class_name="Pco_camera",
            **kwargs,
        )
        self.settings["serial_num"] = 87
        # self.settings["number_of_images"] = 1
        # self.settings["exposure_time"] = 0.1
        self.settings["interface"] = "USB 2.0"


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        labels = {"serial_num": "Serial number", "interface": "Camera interface"}
        super().__init__(
            parent,
            "pco_camera",
            data,
            settings_dict,
            config_dict,
            additional_info,
            labels=labels,
        )
        self.load_settings()
