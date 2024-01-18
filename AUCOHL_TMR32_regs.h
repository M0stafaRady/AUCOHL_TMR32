/*
	Copyright 2024 AUCOHL

	Author: Mohamed Shalan (mshalan@aucegypt.edu)

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

#ifndef AUCOHL_TMR32REGS_H
#define AUCOHL_TMR32REGS_H

#ifndef IO_TYPES
#define IO_TYPES
#define   __R     volatile const unsigned int
#define   __W     volatile       unsigned int
#define   __RW    volatile       unsigned int
#endif

#define AUCOHL_TMR32_CTRL_REG_TE_BIT	0
#define AUCOHL_TMR32_CTRL_REG_TE_MASK	0x1
#define AUCOHL_TMR32_CTRL_REG_TS_BIT	1
#define AUCOHL_TMR32_CTRL_REG_TS_MASK	0x2
#define AUCOHL_TMR32_CTRL_REG_P0E_BIT	2
#define AUCOHL_TMR32_CTRL_REG_P0E_MASK	0x4
#define AUCOHL_TMR32_CTRL_REG_P1E_BIT	3
#define AUCOHL_TMR32_CTRL_REG_P1E_MASK	0x8
#define AUCOHL_TMR32_CTRL_REG_DTE_BIT	4
#define AUCOHL_TMR32_CTRL_REG_DTE_MASK	0x10
#define AUCOHL_TMR32_CTRL_REG_PI0_BIT	5
#define AUCOHL_TMR32_CTRL_REG_PI0_MASK	0x20
#define AUCOHL_TMR32_CTRL_REG_PI1_BIT	6
#define AUCOHL_TMR32_CTRL_REG_PI1_MASK	0x40
#define AUCOHL_TMR32_CFG_REG_DIR_BIT	0
#define AUCOHL_TMR32_CFG_REG_DIR_MASK	0x3
#define AUCOHL_TMR32_CFG_REG_P_BIT	2
#define AUCOHL_TMR32_CFG_REG_P_MASK	0x4
#define AUCOHL_TMR32_PWM0CFG_REG_E0_BIT	0
#define AUCOHL_TMR32_PWM0CFG_REG_E0_MASK	0x3
#define AUCOHL_TMR32_PWM0CFG_REG_E1_BIT	2
#define AUCOHL_TMR32_PWM0CFG_REG_E1_MASK	0xc
#define AUCOHL_TMR32_PWM0CFG_REG_E2_BIT	4
#define AUCOHL_TMR32_PWM0CFG_REG_E2_MASK	0x30
#define AUCOHL_TMR32_PWM0CFG_REG_E3_BIT	6
#define AUCOHL_TMR32_PWM0CFG_REG_E3_MASK	0xc0
#define AUCOHL_TMR32_PWM0CFG_REG_E4_BIT	8
#define AUCOHL_TMR32_PWM0CFG_REG_E4_MASK	0x300
#define AUCOHL_TMR32_PWM0CFG_REG_E5_BIT	10
#define AUCOHL_TMR32_PWM0CFG_REG_E5_MASK	0xc00
#define AUCOHL_TMR32_PWM1CFG_REG_E0_BIT	0
#define AUCOHL_TMR32_PWM1CFG_REG_E0_MASK	0x3
#define AUCOHL_TMR32_PWM1CFG_REG_E1_BIT	2
#define AUCOHL_TMR32_PWM1CFG_REG_E1_MASK	0xc
#define AUCOHL_TMR32_PWM1CFG_REG_E2_BIT	4
#define AUCOHL_TMR32_PWM1CFG_REG_E2_MASK	0x30
#define AUCOHL_TMR32_PWM1CFG_REG_E3_BIT	6
#define AUCOHL_TMR32_PWM1CFG_REG_E3_MASK	0xc0
#define AUCOHL_TMR32_PWM1CFG_REG_E4_BIT	8
#define AUCOHL_TMR32_PWM1CFG_REG_E4_MASK	0x300
#define AUCOHL_TMR32_PWM1CFG_REG_E5_BIT	10
#define AUCOHL_TMR32_PWM1CFG_REG_E5_MASK	0xc00

#define AUCOHL_TMR32_TO_FLAG	0x1
#define AUCOHL_TMR32_MX_FLAG	0x2
#define AUCOHL_TMR32_MY_FLAG	0x4

typedef struct _AUCOHL_TMR32_TYPE_ {
	__R 	TMR;
	__W 	RELOAD;
	__W 	PR;
	__W 	CMPX;
	__W 	CMPY;
	__W 	CTRL;
	__W 	CFG;
	__W 	PWM0CFG;
	__W 	PWM1CFG;
	__W 	PWMDT;
	__R 	reserved[950];
	__RW	im;
	__R 	mis;
	__R 	ris;
	__W 	icr;
} AUCOHL_TMR32_TYPE;

#endif

