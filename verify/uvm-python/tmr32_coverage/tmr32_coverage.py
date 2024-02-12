from uvm.base.uvm_component import UVMComponent
from uvm.macros import uvm_component_utils
from uvm.tlm1.uvm_analysis_port import UVMAnalysisImp
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW 
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.macros.uvm_tlm_defines import uvm_analysis_imp_decl
from EF_UVM.ip_env.ip_coverage.ip_coverage import ip_coverage


class tmr32_coverage(ip_coverage):
    """
    component that initialize the coverage groups and control when to sample the data.
    """
    def __init__(self, name="tmr32_coverage", parent=None):
        super().__init__(name, parent)

    def write(self, tr):
        pass

uvm_component_utils(tmr32_coverage)
