`timescale 1ns/1ps

module top();
wire pwm0;
wire pwm1;
wire pwm_fault = 0;
reg PCLK = 0;
wire PRESETn;
wire [31:0] PADDR;
wire PWRITE;
wire PSEL;
wire PENABLE;
wire [31:0] PWDATA;
wire [31:0] PRDATA;
wire PREADY;
wire irq =0;

AUCOHL_TMR32_APB uut(
    .pwm0(pwm0),
    .pwm1(pwm1),
    .pwm_fault(pwm_fault),
    .PCLK(PCLK),
    .PRESETn(PRESETn),
    .PADDR(PADDR),
    .PWRITE(PWRITE),
    .PSEL(PSEL),
    .PENABLE(PENABLE),
    .PWDATA(PWDATA),
    .PRDATA(PRDATA),
    .PREADY(PREADY)
);

`ifndef SKIP_WAVE_DUMP
initial begin
    $dumpfile("waves.vcd");
    $dumpvars(0, top);
end
`endif

always #5 PCLK = !PCLK;

endmodule