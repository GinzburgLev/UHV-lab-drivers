from .leybold_combivac_IT23_ophyd import Leybold_Combivac_It23

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="leybold_combivac_IT23",
            virtual=False,
            tags=[],
            directory="leybold_combivac_IT23",
            ophyd_device=Leybold_Combivac_It23,
            ophyd_class_name="Leybold_Combivac_It23",
            **kwargs,
        )


#        self.settings["baud_rate"] = 9600
#        self.settings["write_termination"] = "\r"
#        self.settings["read_termination"] = "\r"


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        #        labels = {
        #            "write_termination": "Out-Terminator:"
        #        }
        super().__init__(
            parent,
            "leybold_combivac_IT23",
            data,
            settings_dict,
            config_dict,
            additional_info,
            #            labels=labels,
        )
        self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()
