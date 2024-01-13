`include "aucohl_rtl.vh"
`include "./IP_Utilities/rtl/aucohl_lib.vh"


module AUCOHL_TMR32 (
    input   wire            clk,
    input   wire            rst_n,
    input   wire            tmr_en,
    input   wire            tmr_start,
    input   wire            pwm0_en,
    input   wire            pwm1_en,
    input   wire [31:0]     tmr_reload,
    input   wire [31:0]     cmpx,
    input   wire [31:0]     cmpy,
    input   wire [31:0]     prescaler,
    input   wire [ 2:0]     tmr_cfg,     // [2]: Periodic/OneShot; [1:0]: 10: Up, 01: Down, 11: Up/Down
    input   wire [11:0]     pwm0_cfg,
    input   wire [11:0]     pwm1_cfg,
    input   wire [ 7:0]     pwm_dt,
    input   wire            pwm_dt_en,
    output  wire [31:0]     tmr,
    output  wire            matchx_flag,
    output  wire            matchy_flag,
    output  wire            timeout_flag,
    output  wire            pwm0,
    output  wire            pwm1
);

    wire [1:0]  tmr_mode        = tmr_cfg[1:0];
    wire        tmr_periodic    = tmr_cfg[2];

    reg [31:0]  tmr_reg;
    reg [31:0]  pr_reg;

    wire        tmr_clr;

    wire        tmr_en_pulse = tmr_clr;
    reg         tmr_run;


    aucohl_ped TMREN_PE (
        .clk(clk),
        .in(tmr_en),
        .out(tmr_clr)
    );

    wire tick = (pr_reg == 0);
    `SYNC_BLOCK(clk, rst_n, pr_reg, 1)
        if(tmr_en)
            if(tick) pr_reg <= prescaler; 
            else pr_reg <= pr_reg - 1; 
        else
            pr_reg <= prescaler ;


    reg         tmr_dir;        // 1: Up, 0: Down
    wire        tmr_eq_reload       = (tmr == tmr_reload);
    wire        tmr_eq_zero         = (tmr == 0);
    wire        tmr_eq_reload_m_1   = (tmr == (tmr_reload - 1));
    wire        tmr_eq_one          = (tmr == 1);
    wire        tmr_eq_cmpx         = (tmr == cmpx);
    wire        tmr_eq_cmpy         = (tmr == cmpy);

    `SYNC_BLOCK(clk, rst_n, tmr_run, 0)
        if(tmr_en_pulse)
            tmr_run <= 1;
        else if(~tmr_periodic & tick)
            if((tmr_mode[0] == 1'b1) & tmr_eq_one & ~tmr_dir)
                tmr_run <= 0;
            else if((tmr_mode == 2'b10) & tmr_eq_reload_m_1 & tmr_dir)
                tmr_run <= 1;


    // The timer
    reg [31:0]  tmr_reg_next;

    always@* begin
        tmr_reg_next = tmr_reg;
        if(~tmr_run)
            tmr_reg_next = tmr_reg;    
        else if(tmr_start & (tmr_mode == 2'b01))
            tmr_reg_next = tmr_reload;
        else if(tmr_start & (tmr_mode == 2'b10))
            tmr_reg_next = 0;
        else if(tmr_mode == 2'b11) begin
            if(tmr_dir)
                tmr_reg_next = tmr_reg + 1;
            else
                tmr_reg_next = tmr_reg - 1; 
        end
        else if((tmr_mode == 2'b01))
            if(tmr_eq_zero)
                tmr_reg_next = tmr_periodic ? tmr_reload : tmr_reg;
            else
                tmr_reg_next = tmr_reg_next - 1;    
        else if((tmr_mode == 2'b10))
            if(tmr_eq_reload)
                tmr_reg_next = tmr_periodic ? 0 : tmr_reg;
            else
                tmr_reg_next = tmr_reg_next + 1;
    end

    `SYNC_BLOCK(clk, rst_n, tmr_reg, 0)
    if(tmr_en)
        if(tmr_clr)
            if(tmr_mode == 2'b01)
                tmr_reg = tmr_reload;
            else
                tmr_reg = 0;
        else 
            if(tick)
                tmr_reg <=  tmr_reg_next;

    // The counting direction flag
    `SYNC_BLOCK(clk, rst_n, tmr_dir, 1)
        if(tmr_clr)
            if(tmr_mode == 2'b01)
                tmr_dir = 0;
            else
                tmr_dir = 1;
        else if(tick)
            if(tmr_mode == 2'b11) begin
                if(tmr_eq_one & ~tmr_dir) 
                    tmr_dir <= 1;
                else if(tmr_eq_reload_m_1 & tmr_dir)
                    tmr_dir = 0;
            end
            else if(tmr_mode == 2'b10)
                tmr_dir <= 1'b1;
            else if(tmr_mode == 2'b10)
                tmr_dir <= 1'b0;
            else
                tmr_dir <= 1'b1;

    // PWM
    function pwm_action(input [1:0] action, input sig);
        case (action)
            2'b00: pwm_action = sig;
            2'b01: pwm_action = 0;
            2'b10: pwm_action = 1;
            2'b11: pwm_action = ~sig; 
        endcase
    endfunction 

    reg     pwm0_reg, pwm0_reg_next;
    reg     pwm1_reg, pwm1_reg_next;

    always @* begin
        pwm0_reg_next = pwm0_reg;
        casez({tmr_dir, tmr_eq_zero, tmr_eq_cmpx, tmr_eq_cmpy, tmr_eq_reload})
            5'b?_1_00_0 : pwm0_reg_next = pwm_action(pwm0_cfg[ 1: 0], pwm0_reg);    // U/D, 0
            5'b1_0_10_0 : pwm0_reg_next = pwm_action(pwm0_cfg[ 3: 2], pwm0_reg);    // U, CMPX
            5'b1_0_01_0 : pwm0_reg_next = pwm_action(pwm0_cfg[ 5: 4], pwm0_reg);    // U, CMPY
            5'b?_0_00_1 : pwm0_reg_next = pwm_action(pwm0_cfg[ 7: 6], pwm0_reg);    // U/D, RELOAD
            5'b0_0_01_0 : pwm0_reg_next = pwm_action(pwm0_cfg[ 9: 8], pwm0_reg);    // D, CMPY
            5'b0_0_10_0 : pwm0_reg_next = pwm_action(pwm0_cfg[11:10], pwm0_reg);    // D, CMPX
        endcase        
    end

    always @* begin
        pwm1_reg_next = pwm1_reg;
        casez({tmr_dir, tmr_eq_zero, tmr_eq_cmpx, tmr_eq_cmpy, tmr_eq_reload})
            5'b?_1_00_0 : pwm1_reg_next = pwm_action(pwm1_cfg[ 1: 0], pwm1_reg);    // U/D, 0
            5'b1_0_10_0 : pwm1_reg_next = pwm_action(pwm1_cfg[ 3: 2], pwm1_reg);    // U, CMPX
            5'b1_0_01_0 : pwm1_reg_next = pwm_action(pwm1_cfg[ 5: 4], pwm1_reg);    // U, CMPY
            5'b?_0_00_1 : pwm1_reg_next = pwm_action(pwm1_cfg[ 7: 6], pwm1_reg);    // U/D, RELOAD
            5'b0_0_01_0 : pwm1_reg_next = pwm_action(pwm1_cfg[ 9: 8], pwm1_reg);    // D, CMPY
            5'b0_0_10_0 : pwm1_reg_next = pwm_action(pwm1_cfg[11:10], pwm1_reg);    // D, CMPX
        endcase        
    end

    `SYNC_BLOCK(clk, rst_n, pwm0_reg, 0)
        if(pwm0_en & tick)
            pwm0_reg <= pwm0_reg_next;

    `SYNC_BLOCK(clk, rst_n, pwm1_reg, 0)
        if(pwm1_en & tick)
            pwm1_reg <= pwm1_reg_next;


    // Dead time insertion
    reg pwm0_delayed;
    reg [7:0] dly_cntr;
    `SYNC_BLOCK(clk, rst_n, dly_cntr, 0)
        if(tick)
            if(dly_cntr == 0)
                dly_cntr <= pwm_dt;
            else 
                dly_cntr <= dly_cntr - 1;
                
    `SYNC_BLOCK(clk, rst_n, pwm0_delayed, 0)
        if(tick)
            if(dly_cntr == 0)
                pwm0_delayed <= pwm0_reg;
    
    // Connect the outputs
    wire pwm0_xor = (pwm0_delayed ^ pwm0_reg);
    wire pwm1_xor = (pwm0_delayed ^ ~pwm0_reg);
    
    assign  tmr             =   tmr_reg;
    assign  pwm0            =   pwm_dt_en ? (pwm0_delayed & pwm0_reg) : pwm0_reg;
    assign  pwm1            =   pwm_dt_en ? (~pwm0_delayed & ~pwm0_reg) : pwm1_reg;
    assign  matchx_flag     =   tmr_eq_cmpx;
    assign  matchy_flag     =   tmr_eq_cmpy;
    assign  timeout_flag    =   tmr_dir ? tmr_eq_reload : tmr_eq_zero;
    
endmodule
