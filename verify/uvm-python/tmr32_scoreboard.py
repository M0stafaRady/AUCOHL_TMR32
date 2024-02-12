from uvm.comps import UVMScoreboard
from uvm.macros import uvm_component_utils, uvm_info, uvm_error
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW
from EF_UVM.scoreboard import scoreboard
from cocotb.queue import Queue
from tmr32_item.tmr32_item import tmr32_pwm_item, tmr32_tmr_item
import cocotb
from cocotb.triggers import Combine
#  TODO: replace this with callback in the future


class tmr32_scoreboard(scoreboard):
    """to compare the pwm with pwm and tmr with tmr"""
    def __init__(self, name="tmr32_scoreboard", parent=None):
        super().__init__(name, parent)
        self.q_pwm = Queue()
        self.q_pwm_vip = Queue()
        self.q_tmr = Queue()
        self.q_tmr_vip = Queue()

    def write_ip(self, tr):
        uvm_info(self.tag, "write_ip: " + tr.convert2string(), UVM_MEDIUM)
        if type(tr) is tmr32_tmr_item:
            self.q_tmr.put_nowait(tr)
        elif type(tr) is tmr32_pwm_item:
            self.q_pwm.put(tr)
            
    def write_ip_vip(self, tr):
        uvm_info(self.tag, "write_ip_vip: " + tr.convert2string(), UVM_MEDIUM)
        if type(tr) is tmr32_tmr_item:
            self.q_tmr_vip.put_nowait(tr)
        elif type(tr) is tmr32_pwm_item:
            self.q_pwm_vip.put(tr)

    async def checker_ip(self):
        pwm = await cocotb.start(self.checker_pwm())
        tmr = await cocotb.start(self.checker_tmr())
        await Combine(pwm, tmr)
    
    async def checker_pwm(self):
        while True:
            val = await self.q_pwm.get()
            exp = await self.q_pwm_vip.get()
            if not val.do_compare(exp):
                uvm_error(self.tag, "IP mismatch: " + val.convert2string() + " != " + exp.convert2string())

    async def checker_tmr(self):
        while True:
            val = await self.q_pwm.get()
            exp = await self.q_pwm_vip.get()
            if not val.do_compare(exp):
                uvm_error(self.tag, "IP mismatch: " + val.convert2string() + " != " + exp.convert2string())

    def extract_phase(self, phase):
        super().extract_phase(phase)
        if self.q_pwm.qsize() not in [0, 1] or self.q_pwm_vip.qsize() not in [0, 1]:
            uvm_error(self.tag, f"PWM queue still have unchecked items queue ip {self.q_pwm._queue} size {self.q_pwm.qsize()} ip_vip {self.q_pwm_vip._queue} size {self.q_pwm_vip.qsize()}")
        if self.q_tmr.qsize() not in [0, 1] or self.q_tmr_vip.qsize() not in [0, 1]:
            uvm_error(self.tag, f"TMR queue still have unchecked items queue ip {self.q_tmr._queue} size {self.q_tmr.qsize()} ip_vip {self.q_tmr_vip._queue} size {self.q_tmr_vip.qsize()}")


uvm_component_utils(tmr32_scoreboard)
