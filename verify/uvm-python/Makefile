PLUSARGS += "+UVM_VERBOSITY=UVM_MEDIUM"
TOPLEVEL := top
MODULE   ?= top_module
VERILOG_SOURCES ?=  $(PWD)/top.v $(PWD)/../../hdl/rtl/bus_wrappers/AUCOHL_TMR32_APB.v  $(PWD)/../../hdl/rtl/AUCOHL_TMR32.v
RTL_MACROS ?= ""
YAML_FILE = $(PWD)/../../AUCOHL_TMR32.yaml
MAKEFLAGS += --no-print-directory

# List of tests
TESTS := tmr32_Try time_vary_test
TESTS := time_vary_test

# Variable for tag - set this as required
SIM_TAG ?= default_tag

# Define SIM_PATH variable
SIM_PATH := $(PWD)/sim/$(SIM_TAG)

include EF_UVM/Makefile.test
