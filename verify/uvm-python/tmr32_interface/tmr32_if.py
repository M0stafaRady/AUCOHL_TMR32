from uvm.base.sv import sv_if


class tmr32_if(sv_if):

    #  // Actual Signals
    # wire 		pwm0;
    # wire 		pwm1;

    def __init__(self, dut):
        bus_map = {"PCLK": "PCLK", "pwm0": "pwm0", "pwm1": "pwm1"}
        super().__init__(dut, "", bus_map)
