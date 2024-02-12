from EF_UVM.ip_env.ip_logger.ip_logger import ip_logger
import cocotb 
from uvm.macros import uvm_component_utils


class tmr32_logger(ip_logger):
    def __init__(self, name="tmr32_logger", parent=None):
        super().__init__(name, parent)
        self.header = ['Time (ns)', 'Source', 'Pattern']
        self.col_widths = [10]* len(self.header)

    def logger_formatter(self, transaction):
        sim_time = f"{cocotb.utils.get_sim_time(units='ns')} ns"
        source = f"{transaction.source}"
        pattern = f"{transaction.pattern}"
        return [sim_time, source, pattern]


uvm_component_utils(tmr32_logger)
