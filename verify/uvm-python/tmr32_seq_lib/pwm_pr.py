from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_fatal, uvm_info
from EF_UVM.wrapper_env.wrapper_item import wrapper_bus_item
from uvm.base.uvm_config_db import UVMConfigDb
from cocotb.triggers import Timer
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
import random
from tmr32_seq_lib.timer_config import timer_config
from EF_UVM.wrapper_env.wrapper_seq_lib.reset_seq import reset_seq
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW, UVM_HIGH
from cocotb_coverage.coverage import coverage_db


class pwm_pr(timer_config):

    def __init__(self, name="pwm_pr"):
        super().__init__(name)
        self.monitor = None

    async def body(self):
        # get register names/address conversion dict
        await super().body()
        pr_ranges = self.get_uncovered_pr()
        for pr_range in pr_ranges:
            await self.config_diffrent_pr(pr_range)
            for i in range(2):
                await self.monitor.detect_pattern_event.wait()
                self.monitor.detect_pattern_event.clear()
            await self.stop_timer()
            await uvm_do(self, reset_seq())

    async def config_diffrent_pr(self, pr_range = [0, 0x6]):
        await self.set_timer_pr(pr_range)
        await self.set_pwm_actions()
        await self.config_timer_regs()
        await self.set_timer_mode(is_periodic=1)
        await self.start_timer(pwm_enable=[1, 1])

    async def set_pwm_actions(self):
        # add condition to make sure output would be generated not all ones or all zeros
        condition = lambda data: 0b11 in [data >> i & 0b11 for i in range(0, data.bit_length(), 2)]  or all(i in [data >> i & 0b11 for i in range(0, data.bit_length(), 2)]  for i in [0b10, 0b01]) # at least inverted exists or high and low exists
        await self.send_req(is_write=True, reg="PWM0CFG", data_condition=condition) # should start with high or low not realistic to start with no change or invert
        await self.send_req(is_write=True, reg="PWM1CFG", data_condition=condition)
    
    def get_uncovered_pr(self):
        detailed_coverage = coverage_db["top.tmr32.pwm.Prescaler"].detailed_coverage
        ranges = []
        for bin, value in detailed_coverage.items():
            if value == 0:
                ranges.append(bin)
                uvm_info(self.tag, f"bin {bin} not covered", UVM_LOW)
        return ranges


uvm_object_utils(pwm_pr)
