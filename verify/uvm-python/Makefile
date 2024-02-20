PLUSARGS += "+UVM_VERBOSITY=UVM_MEDIUM"
TOPLEVEL := top
MODULE   ?= top_module
VERILOG_SOURCES ?=  $(PWD)/top.v $(PWD)/../../hdl/rtl/bus_wrappers/AUCOHL_TMR32_APB.v  $(PWD)/../../hdl/rtl/AUCOHL_TMR32.v
RTL_MACROS ?= ""
YAML_FILE = $(PWD)/../../AUCOHL_TMR32.yaml
MAKEFLAGS += --no-print-directory

# List of tests
TESTS := tmr32_Try time_vary_test pwm_pr_test
TESTS := pwm_pr_test

# Variable for tag - set this as required
SIM_TAG ?= default_tag

# Define SIM_PATH variable
SIM_PATH := $(PWD)/sim/$(SIM_TAG)

REPO_DIR := EF_UVM

clone_ef_uvm := $(shell if [ ! -d "$(REPO_DIR)" ]; then \
	echo "Cloning the EF_UVM repository..."; \
	git clone https://github.com/M0stafaRady/EF_UVM.git; \
fi;)

include EF_UVM/Makefile.test
