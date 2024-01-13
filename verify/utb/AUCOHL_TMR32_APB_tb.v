/*
	Copyright 2024 AUCOHL

	Author: Mohamed Shalan (<email>)

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	    http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.

*/

/* THIS FILE IS GENERATED, edit it to complete the testbench */

`timescale		1ns/1ps

`default_nettype	none

`define			APB_AW			16
`define			MS_TB_SIMTIME		1_000_000

`include		"tb_macros.vh"

module AUCOHL_TMR32_APB_tb;

	// Change the following parameters as desired
	parameter real CLOCK_PERIOD = 100.0;
	parameter real RESET_DURATION = 999.0;

	// DON NOT Change the following parameters
	localparam [`APB_AW-1:0]
				TMR_REG_OFFSET =        `APB_AW'h0000,
				RELOAD_REG_OFFSET =     `APB_AW'h0004,
				PR_REG_OFFSET = `APB_AW'h0008,
				CMPX_REG_OFFSET =       `APB_AW'h000c,
				CMPY_REG_OFFSET =       `APB_AW'h0010,
				CTRL_REG_OFFSET =       `APB_AW'h0014,
				CFG_REG_OFFSET =        `APB_AW'h0018,
				PWM0CFG_REG_OFFSET =    `APB_AW'h001c,
				PWM1CFG_REG_OFFSET =    `APB_AW'h0020,
				PWMDT_REG_OFFSET =      `APB_AW'h0024,
				IM_REG_OFFSET =         `APB_AW'h0f00,
				IC_REG_OFFSET =         `APB_AW'h0f0c,
				RIS_REG_OFFSET =        `APB_AW'h0f08,
				MIS_REG_OFFSET =        `APB_AW'h0f04;

	`TB_APB_SIG

	wire	[0:0]	pwm0;
	wire	[0:0]	pwm1;

	`TB_CLK(PCLK, CLOCK_PERIOD)
	`TB_ESRST(PRESETn, 1'b0, PCLK, RESET_DURATION)
	`TB_DUMP("APB_AUCOHL_TMR32_tb.vcd", AUCOHL_TMR32_APB_tb, 0)
	`TB_FINISH(`MS_TB_SIMTIME)

	AUCOHL_TMR32_APB DUV (
		`TB_APB_SLAVE_CONN,
		.pwm0(pwm0),
		.pwm1(pwm1)
	);

	`include "apb_tasks.vh"

	`TB_TEST_EVENT(test1)
	`TB_TEST_EVENT(test2)
	`TB_TEST_EVENT(test3)
	`TB_TEST_EVENT(test4)
	`TB_TEST_EVENT(test5)
	`TB_TEST_EVENT(test6)
	`TB_TEST_EVENT(test7)
	`TB_TEST_EVENT(test8)

	initial begin
		#999 -> e_assert_reset;
		@(e_reset_done);

		// Perform Test 1
		#1000 -> e_test1_start;
		@(e_test1_done);

		// Perform Test 1
		#1000 -> e_test2_start;
		@(e_test2_done);

		// Perform Test 3
		#1000 -> e_test3_start;
		@(e_test3_done);

		// Perform Test 4
		#1000 -> e_test4_start;
		@(e_test4_done);

		// Perform Test 6
		#1000 -> e_test6_start;
		@(e_test6_done);

		// Perform Test 5
		#1000 -> e_test5_start;
		@(e_test5_done);

		// Perform Test 7
		#1000 -> e_test7_start;
		@(e_test7_done);

		// Perform Test 8
		#1000 -> e_test8_start;
		@(e_test8_done);

		// Finish the simulation
		#1000 $finish();
	end


	// Test 1 - Periodic U/D
	`TB_TEST_BEGIN(test1)
		// Test 1 code goes here
		// Reload is 10
		APB_W_WRITE(RELOAD_REG_OFFSET, 32'd10);
		// Set the prescaler to 4 (divide the clock by 5)
		APB_W_WRITE(PR_REG_OFFSET, 32'd4);
		// Periodic Up/Down 
		APB_W_WRITE(CFG_REG_OFFSET, 3'b1_11);
		// Enable the timer
		APB_W_WRITE(CTRL_REG_OFFSET, 4'b0001);
		// Wait for some time 
		#20_000;
		// Observe the behavior on the waveform viewer: /\/\ 0->10->0
	`TB_TEST_END(test1)

	// Test 2 - Periodic U
	`TB_TEST_BEGIN(test2)
		// Disable the timer
		APB_W_WRITE(CTRL_REG_OFFSET, 4'b0000);
		// Reload is 20
		APB_W_WRITE(RELOAD_REG_OFFSET, 32'd20);
		// Set the prescaler to 3 (divide the clock by 4)
		APB_W_WRITE(PR_REG_OFFSET, 32'd4);
		// Periodic Up
		APB_W_WRITE(CFG_REG_OFFSET, 3'b1_10);
		// Enable the timer
		APB_W_WRITE(CTRL_REG_OFFSET, 4'b0001);
		// Wait for some time 
		#25_000;
		// Observe the behavior on the waveform viewer: /|/| 0->20
	`TB_TEST_END(test2)
	
	// Test 3 - Periodic D
	`TB_TEST_BEGIN(test3)
		// Disable the timer
		APB_W_WRITE(CTRL_REG_OFFSET, 4'b0000);
		// Reload is 15
		APB_W_WRITE(RELOAD_REG_OFFSET, 32'd15);
		// Set the prescaler to 2 (divide the clock by 3)
		APB_W_WRITE(PR_REG_OFFSET, 32'd3);
		// Periodic Down 
		APB_W_WRITE(CFG_REG_OFFSET, 3'b1_01);
		// Enable the timer
		APB_W_WRITE(CTRL_REG_OFFSET, 4'b0001);
		// Wait for some time 
		#25_000;
		// Observe the behavior on the waveform viewer: |\|\ 15->0
	`TB_TEST_END(test3)

	// Test 4 - One Shot U/D 
	`TB_TEST_BEGIN(test4)
		// Disable the timer
		APB_W_WRITE(CTRL_REG_OFFSET, 4'b0000);
		// Reload is 15
		APB_W_WRITE(RELOAD_REG_OFFSET, 32'd15);
		// Set the prescaler to 2 (divide the clock by 3)
		APB_W_WRITE(PR_REG_OFFSET, 32'd2);
		// One-shot Up/Down 
		APB_W_WRITE(CFG_REG_OFFSET, 3'b0_11);
		// Enable the timer
		APB_W_WRITE(CTRL_REG_OFFSET, 4'b0001);
		// Wait for some time 
		#25_000;
		// Observe the behavior on the waveform viewer: /\ 0->15->0
	`TB_TEST_END(test4)
	
	// Test 5 - One Shot U 
	`TB_TEST_BEGIN(test5)
		// Disable the timer
		APB_W_WRITE(CTRL_REG_OFFSET, 4'b0000);
		// Reload is 15
		APB_W_WRITE(RELOAD_REG_OFFSET, 32'd15);
		// Set the prescaler to 2 (divide the clock by 3)
		APB_W_WRITE(PR_REG_OFFSET, 32'd2);
		// One shot Up
		APB_W_WRITE(CFG_REG_OFFSET, 3'b0_10);
		// Enable the timer
		APB_W_WRITE(CTRL_REG_OFFSET, 4'b0001);
		// Wait for some time 
		#25_000;
		// Observe the behavior on the waveform viewer: /| 0->15
	`TB_TEST_END(test5)

	// Test 6 - One Shot D 
	`TB_TEST_BEGIN(test6)
		// Disable the timer
		APB_W_WRITE(CTRL_REG_OFFSET, 4'b0000);
		// Reload is 15
		APB_W_WRITE(RELOAD_REG_OFFSET, 32'd15);
		// Set the prescaler to 2 (divide the clock by 3)
		APB_W_WRITE(PR_REG_OFFSET, 32'd2);
		// One-shot Down 
		APB_W_WRITE(CFG_REG_OFFSET, 3'b0_01);
		// Enable the timer
		APB_W_WRITE(CTRL_REG_OFFSET, 4'b0001);
		// Wait for some time 
		#25_000;
		// Observe the behavior on the waveform viewer: |\ 15->0
	`TB_TEST_END(test6)

	// Test 7 - PWM
	`TB_TEST_BEGIN(test7)
		// Disable the timer
		APB_W_WRITE(CTRL_REG_OFFSET, 4'b0000);
		// Reload is 10
		APB_W_WRITE(RELOAD_REG_OFFSET, 32'd10);
		// Set the prescaler to 1 (divide the clock by 2)
		APB_W_WRITE(PR_REG_OFFSET, 32'd1);
		// Periodic Up/Down 
		APB_W_WRITE(CFG_REG_OFFSET, 3'b1_11);
		// CMPX is 4
		APB_W_WRITE(CMPX_REG_OFFSET, 32'd3);
		// CMPY is 5
		APB_W_WRITE(CMPY_REG_OFFSET, 32'd7);
		// Configure PMW0
		APB_W_WRITE(PWM0CFG_REG_OFFSET, 12'b01_00_10_00_01_10);
		// Configure PMW1
		APB_W_WRITE(PWM1CFG_REG_OFFSET, 12'b10_11_11_11_11_10);
		// Enable the timer & both PMW channels
		APB_W_WRITE(CTRL_REG_OFFSET, 4'b11_0_1);
		// Wait for some time 
		#25_000;
		// Observe the behavior on the waveform viewer: |\ 15->0
	`TB_TEST_END(test7)

	// Test 8 - PWM with inversion and deadtime
	`TB_TEST_BEGIN(test8)
		// Disable the timer
		APB_W_WRITE(CTRL_REG_OFFSET, 5'b00000);
		// Reload is 20
		APB_W_WRITE(RELOAD_REG_OFFSET, 32'd20);
		// Set the prescaler to 1 (divide the clock by 2)
		APB_W_WRITE(PR_REG_OFFSET, 32'd1);
		// Periodic Up/Down 
		APB_W_WRITE(CFG_REG_OFFSET, 3'b1_11);
		// CMPX is 4
		APB_W_WRITE(CMPX_REG_OFFSET, 32'd10);
		// CMPY is 5
		APB_W_WRITE(CMPY_REG_OFFSET, 32'd14);
		// Configure PMW0
		APB_W_WRITE(PWM0CFG_REG_OFFSET, 12'b01_00_00_00_10_01);
		// Configure PMW1
		APB_W_WRITE(PWM1CFG_REG_OFFSET, 12'b10_11_11_11_11_10);
		// Set the deadtime to 2 (1 = 2 - 1)
		APB_W_WRITE(PWMDT_REG_OFFSET, 1);
		// Enable the timer and PWM0; also, enable the deadtime
		APB_W_WRITE(CTRL_REG_OFFSET, 5'b1_01_0_1);
		// Wait for some time 
		#25_000;
		// Observe the behavior on the waveform viewer: |\ 15->0
	`TB_TEST_END(test8)

endmodule
