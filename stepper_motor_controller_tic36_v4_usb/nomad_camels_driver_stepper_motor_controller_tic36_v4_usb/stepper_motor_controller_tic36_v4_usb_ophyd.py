from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
from ophyd import Device
import subprocess
import yaml
import re
import time


class Stepper_Motor_Controller_Tic36_V4_Usb(Device):
    time_before_repeat = 0.5
    max_position_unchanged_counter = 6

    max_speed = Cpt(
        Custom_Function_Signal,
        name="max_speed",
        kind="config",
        metadata={
            "units": "p/sec",
            "description": "config speed limit for stepper motor in pulses per second",
        },
    )

    max_accel = Cpt(
        Custom_Function_Signal,
        name="max_accel",
        kind="config",
        metadata={
            "units": "p/sec^2",
            "description": "config acceleration limit for stepper motor in pulses per second squared",
        },
    )

    step_mode_set = Cpt(
        Custom_Function_Signal,
        name="step_mode_set",
        kind="config",
        metadata={"units": "", "description": "choose a step mode"},
    )

    current_limit = Cpt(
        Custom_Function_Signal,
        name="current_limit",
        kind="config",
        metadata={
            "units": "mA",
            "description": "choose current limit - defines torque",
        },
    )

    energize = Cpt(
        Custom_Function_Signal,
        name="energize_read",
        kind="config",
        metadata={"units": "", "description": "check or choose if motor is energized"},
    )

    read_device_info = Cpt(
        Custom_Function_SignalRO,
        name="read_device_info",
        metadata={"units": "", "description": "device information"},
    )

    read_VIN_voltage = Cpt(
        Custom_Function_SignalRO,
        name="read_VIN_voltage",
        metadata={
            "units": "",
            "description": "voltage at the VIN pin of the controller",
        },
    )

    read_current_position = Cpt(
        Custom_Function_SignalRO,
        name="read_current_position",
        metadata={"units": "", "description": "read current position of the motor"},
    )

    read_current_velocity = Cpt(
        Custom_Function_SignalRO,
        name="read_current_velocity",
        metadata={"units": "", "description": "read current velocity of the motor"},
    )

    read_target_position = Cpt(
        Custom_Function_SignalRO,
        name="read_target_position",
        metadata={"units": "", "description": "read target position of the motor"},
    )

    set_position = Cpt(
        Custom_Function_Signal,
        name="set_position",
        metadata={"units": "", "description": "set new target position"},
    )

    halt_motor = Cpt(
        Custom_Function_Signal,
        name="halt_motor",
        metadata={"units": "", "description": "emergency stop motor if True"},
    )

    read_errors_string = Cpt(
        Custom_Function_SignalRO,
        name="errors_string",
        metadata={"units": "", "description": "read string describing current errors"},
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
        serial_num="",
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
        self.read_device_info.read_function = self.read_device_info_read_function
        self.read_VIN_voltage.read_function = self.read_VIN_voltage_read_function
        self.read_current_position.read_function = (
            self.read_current_position_read_function
        )
        self.read_current_velocity.read_function = (
            self.read_current_velocity_read_function
        )
        self.read_target_position.read_function = (
            self.read_target_position_read_function
        )
        self.read_errors_string.read_function = self.read_errors_string_read_function
        self.max_speed.put_function = self.max_speed_put_function
        self.max_accel.put_function = self.max_accel_put_function
        self.step_mode_set.put_function = self.step_mode_set_put_function
        self.current_limit.put_function = self.current_limit_put_function
        self.energize.put_function = self.energize_put_function
        self.set_position.put_function = self.set_position_put_function
        self.halt_motor.put_function = self.halt_motor_put_function
        if name == "test":
            return

    def ticcmd(self, *args):
        return subprocess.check_output(["ticcmd", "-d", self.serial_num] + list(args))

    def read_full_status(self):
        return yaml.safe_load(self.ticcmd("-s", "--full"))

    def read_device_info_read_function(self):
        full_status_dict = self.read_full_status()
        info_str = (
            full_status_dict["Name"]
            + ", firmware version "
            + str(full_status_dict["Firmware version"])
            + ", up for "
            + str(full_status_dict["Up time"])
            + "s"
        )
        # print(f"Device info: {info_str}")
        return info_str

    def read_VIN_voltage_read_function(self):
        full_status_dict = self.read_full_status()
        VIN_voltage_str = full_status_dict["VIN voltage"]
        VIN_voltage_num = float("".join(re.findall(r"[\.\d]", VIN_voltage_str)))
        # print(f"VIN voltage = {VIN_voltage_num} V")
        return VIN_voltage_num

    def read_current_position_read_function(self):
        full_status_dict = self.read_full_status()
        current_pos_num = full_status_dict["Current position"]
        # print(f"Current position: {current_pos_num}")
        return current_pos_num

    def read_current_velocity_read_function(self):
        full_status_dict = self.read_full_status()
        current_vel_num = full_status_dict["Current velocity"]
        # print(f"Current velocity: {current_vel_num}")
        return current_vel_num

    def read_target_position_read_function(self):
        full_status_dict = self.read_full_status()
        target_pos_num = full_status_dict["Acting target position"]
        # print(f"Target position: {target_pos_num}")
        return target_pos_num

    def read_errors_string_read_function(self):
        full_status_dict = self.read_full_status()
        errors_list = full_status_dict["Errors currently stopping the motor"]
        errors_str = ", ".join(errors_list)
        # print(f"List of errors: {errors_str}")
        return errors_str

    def max_speed_put_function(self, value):
        self.ticcmd(
            "--max-speed", str(int(value * 10000))
        )  # conversion into steps per second

    def max_accel_put_function(self, value):
        self.ticcmd(
            "--max-accel", str(int(value * 100))
        )  # conversion into steps per second per second
        self.ticcmd("--max-decel", str(int(value * 100)))

    def step_mode_set_put_function(self, value):
        value_rounded = round(value)
        temp = list(range(9))
        acceptable_values = temp
        for i in temp:
            acceptable_values[i] = 2**i
        if value_rounded in acceptable_values:
            if value_rounded == 1:
                self.ticcmd("--step-mode", "full")
            else:
                self.ticcmd("--step-mode", str(value_rounded))
        else:
            print(f"this step mode value can not be accepted")

    def current_limit_put_function(self, value):
        value_rounded = round(value)
        self.ticcmd("--current", str(value_rounded))
        time.sleep(0.01)
        full_status_dict = self.read_full_status()
        current_lim_new = full_status_dict["Current limit"]
        print(f"new current limit of the stepper motor: {current_lim_new}")

    def energize_put_function(self, value):
        if value:
            self.ticcmd("--energize")
        else:
            self.ticcmd("--deenergize")

    def set_position_put_function(self, value):
        current_pos_num = self.read_current_position_read_function()
        current_pos_num_new = current_pos_num
        position_unchanged_counter = 0
        value_int = int(value)
        error_str = self.read_errors_string_read_function()
        error_list = error_str.split(", ")
        try:
            error_list.remove("Command timeout")
            error_list.remove("Safe start violation")
        except:
            print("Can not read motor status")
        if error_list:
            print("Check motor power or errors")
        if value_int == current_pos_num:
            return
        elif value_int > current_pos_num:
            while (value_int > current_pos_num) and (
                position_unchanged_counter < self.max_position_unchanged_counter
            ):
                self.ticcmd("--exit-safe-start", "--position", str(value_int))
                time.sleep(self.time_before_repeat)
                current_pos_num_new = self.read_current_position_read_function()
                if current_pos_num_new == current_pos_num:
                    position_unchanged_counter += 1
                else:
                    position_unchanged_counter = 0
                current_pos_num = current_pos_num_new
        else:
            while (value_int < current_pos_num) and (
                position_unchanged_counter < self.max_position_unchanged_counter
            ):
                self.ticcmd("--exit-safe-start", "--position", str(value_int))
                time.sleep(self.time_before_repeat)
                current_pos_num_new = self.read_current_position_read_function()
                if current_pos_num_new == current_pos_num:
                    position_unchanged_counter += 1
                else:
                    position_unchanged_counter = 0
                current_pos_num = current_pos_num_new

    def halt_motor_put_function(self, value):
        if value:
            self.ticcmd("--halt-and-hold")
            print(f"emergency stop")
        else:
            print(f"no emergency stop")
