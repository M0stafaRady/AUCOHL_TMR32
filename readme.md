# AUCOHL_TMR32

A 32-bit timer and PWM generator with the following features:
- 32-bit prescaler
- Up Counting, Down Counting and Up/Down Counting
- One-shot and Periodic
- Two independent PWM channels with two compare registers
- Configurable PWM dead time/band to generate PWM signals such as those required by a half-H bridge driver
- Fault handeling

## Registers

|Name|Offset|Reset Value|Access Mode|Description|
|---|---|---|---|---|
|TMR|0000|0x00000000|r|The current value of the Timer.|
|RELOAD|0004|0x00000000|w|The timer reload value. In up counting it is used as the terminal count. For down counting it is used as the initial count.|
|PR|0008|0x00000000|w|The Prescaler. The timer counting frequency is $Clock\ freq/(PR + 1)$|
|CMPX|000c|0x00000000|w|Compare Register X.|
|CMPY|0010|0x00000000|w|Compare Register Y.|
|CTRL|0014|0x00000000|w|Control Register.|
|CFG|0018|0x00000000|w|Configuration Register.|
|PWM0CFG|001c|0x00000000|w|PWM0 Configuration Register.|
|PWM1CFG|0020|0x00000000|w|PWM1 Configuration Register.|
|PWMDT|0024|0x00000000|w|PWM deadtime Register.|
|IM|0f00|0x00000000|w|Interrupt Mask Register; write 1/0 to enable/disable interrupts; check the interrupt flags table for more details|
|RIS|0f08|0x00000000|w|Raw Interrupt Status; reflects the current interrupts status;check the interrupt flags table for more details|
|MIS|0f04|0x00000000|w|Masked Interrupt Status; On a read, this register gives the current masked status value of the corresponding interrupt. A write has no effect; check the interrupt flags table for more details|
|IC|0f0c|0x00000000|w|Interrupt Clear Register; On a write of 1, the corresponding interrupt (both raw interrupt and masked interrupt, if enabled) is cleared; check the interrupt flags table for more details|

### TMR Register [Offset: 0x0, mode: r]

The current value of the Timer.
<img src="https://svg.wavedrom.com/{reg:[{name:'TMR', bits:32},{bits: 0}], config: {lanes: 2, hflip: true}} "/>


### RELOAD Register [Offset: 0x4, mode: w]

The timer reload value. In up counting it is used as the terminal count. For down counting it is used as the initial count.
<img src="https://svg.wavedrom.com/{reg:[{name:'RELOAD', bits:32},{bits: 0}], config: {lanes: 2, hflip: true}} "/>


### PR Register [Offset: 0x8, mode: w]

The Prescaler. The timer counting frequency is $Clock\ freq/(PR + 1)$
<img src="https://svg.wavedrom.com/{reg:[{name:'PR', bits:32},{bits: 0}], config: {lanes: 2, hflip: true}} "/>


### CMPX Register [Offset: 0xc, mode: w]

Compare Register X.
<img src="https://svg.wavedrom.com/{reg:[{name:'CMPX', bits:32},{bits: 0}], config: {lanes: 2, hflip: true}} "/>


### CMPY Register [Offset: 0x10, mode: w]

Compare Register Y.
<img src="https://svg.wavedrom.com/{reg:[{name:'CMPY', bits:32},{bits: 0}], config: {lanes: 2, hflip: true}} "/>


### CTRL Register [Offset: 0x14, mode: w]

Control Register.
<img src="https://svg.wavedrom.com/{reg:[{name:'TE', bits:1},{name:'TS', bits:1},{name:'P0E', bits:1},{name:'P1E', bits:1},{name:'DTE', bits:1},{name:'PI0', bits:1},{name:'PI1', bits:1},{bits: 25}], config: {lanes: 2, hflip: true}} "/>

|bit|field name|width|description|
|---|---|---|---|
|0|TE|1|Timer enable|
|1|TS|1|Timer re-start; used in the one-shot mode to restart the timer. Write 1 then 0 to re-start the timer.|
|2|P0E|1|PWM 0 enable|
|3|P1E|1|PWM 1 enable|
|4|DTE|1|PWM deadtime enable|
|5|PI0|1|Invert PWM0 output|
|6|PI1|1|Invert PWM1 output|


### CFG Register [Offset: 0x18, mode: w]

Configuration Register.
<img src="https://svg.wavedrom.com/{reg:[{name:'DIR', bits:2},{name:'P', bits:1},{bits: 29}], config: {lanes: 2, hflip: true}} "/>

|bit|field name|width|description|
|---|---|---|---|
|0|DIR|2|Count direction; 10: Up, 01: Down, 11: Up/Down|
|2|P|1|1: Peiodic, 0: One Shot|


### PWM0CFG Register [Offset: 0x1c, mode: w]

PWM0 Configuration Register.
<img src="https://svg.wavedrom.com/{reg:[{name:'E0', bits:2},{name:'E1', bits:2},{name:'E2', bits:2},{name:'E3', bits:2},{name:'E4', bits:2},{name:'E5', bits:2},{bits: 20}], config: {lanes: 2, hflip: true}} "/>

|bit|field name|width|description|
|---|---|---|---|
|0|E0|2|PWM0 action for matching zero. 00: No Action, 01: Low, 10: High, 11: Invert|
|2|E1|2|PWM0 action for matching CMPX (going up). 00: No Action, 01: Low, 10: High, 11: Invert|
|4|E2|2|PWM0 action for matching CMPY (going up). 00: No Action, 01: Low, 10: High, 11: Invert|
|6|E3|2|PWM0 action for matching RELOAD. 00: No Action, 01: Low, 10: High, 11: Invert|
|8|E4|2|PWM0 action for being matching CMPY (going down). 00: No Action, 01: Low, 10: High, 11: Invert|
|10|E5|2|PWM0 action for being matching CMPX (going down). 00: No Action, 01: Low, 10: High, 11: Invert|


### PWM1CFG Register [Offset: 0x20, mode: w]

PWM1 Configuration Register.
<img src="https://svg.wavedrom.com/{reg:[{name:'E0', bits:2},{name:'E1', bits:2},{name:'E2', bits:2},{name:'E3', bits:2},{name:'E4', bits:2},{name:'E5', bits:2},{bits: 20}], config: {lanes: 2, hflip: true}} "/>

|bit|field name|width|description|
|---|---|---|---|
|0|E0|2|PWM1 action for matching zero. 00: No Action, 01: Low, 10: High, 11: Invert|
|2|E1|2|PWM1 action for matching CMPX (going up). 00: No Action, 01: Low, 10: High, 11: Invert|
|4|E2|2|PWM1 action for matching CMPY (going up). 00: No Action, 01: Low, 10: High, 11: Invert|
|6|E3|2|PWM1 action for matching RELOAD. 00: No Action, 01: Low, 10: High, 11: Invert|
|8|E4|2|PWM1 action for being matching CMPY (going down). 00: No Action, 01: Low, 10: High, 11: Invert|
|10|E5|2|PWM1 action for being matching CMPX (going down). 00: No Action, 01: Low, 10: High, 11: Invert|


### PWMDT Register [Offset: 0x24, mode: w]

PWM deadtime Register.
<img src="https://svg.wavedrom.com/{reg:[{name:'PWMDT', bits:8},{bits: 24}], config: {lanes: 2, hflip: true}} "/>


## Interrupt Flags


The following are the bit definitions for the interrupt registers: IM, RIS, MIS, and IC.

|Bit|Flag|Width|Description|
|---|---|---|---|
|0|TO|1|Timeout; TMR matches 0 (down clounting) or RELOAD (up counting).|
|1|MX|1|TMR matches CMPX register.|
|2|MY|1|TMR matches CMPY register.|