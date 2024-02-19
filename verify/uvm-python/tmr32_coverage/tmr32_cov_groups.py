from uvm.macros.uvm_message_defines import uvm_info
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW
from cocotb_coverage.coverage import CoverPoint, CoverCross
from uvm.macros import uvm_component_utils
from tmr32_item.tmr32_item import tmr32_pwm_item


class tmr32_cov_groups():
    def __init__(self, hierarchy, regs) -> None:
        self.hierarchy = hierarchy
        self.regs = regs
        self.actions = self.actions_combinations()
        self.ip_cov(None, do_sampling=False)

    def ip_cov(self, tr, do_sampling=True):
        @self.apply_decorators(decorators=self.actions)
        @CoverPoint(
            f"{self.hierarchy}.Prescaler",
            xf=lambda tr: (self.regs.read_reg_value("PR")),
            bins=[( i*10 , (i+1)*10) for i in range(10)],
            bins_labels=[(i*10 , (i+1)*10) for i in range(10)],
            at_least=3,
            rel=lambda val, b: b[0] <= val <= b[1]
        )
        @CoverPoint(
            f"{self.hierarchy}.Relaod",
            xf=lambda tr: (self.regs.read_reg_value("RELOAD")),
            bins=[( i*1000 , (i+1)*1000) for i in range(5)],
            bins_labels=[( i*1000 , (i+1)*1000) for i in range(5)],
            at_least=3,
            rel=lambda val, b: b[0] <= val <= b[1]
        )
        @CoverPoint(
            f"{self.hierarchy}.Compare Reg X",
            xf=lambda tr: (self.regs.read_reg_value("CMPX")),
            bins=[( i*1000 , (i+1)*1000) for i in range(5)],
            bins_labels=[( i*1000 , (i+1)*1000) for i in range(5)],
            at_least=3,
            rel=lambda val, b: b[0] <= val <= b[1]
        )
        @CoverPoint(
            f"{self.hierarchy}.Compare Reg Y",
            xf=lambda tr: (self.regs.read_reg_value("CMPX")),
            bins=[( i*1000 , (i+1)*1000) for i in range(5)],
            bins_labels=[( i*1000 , (i+1)*1000) for i in range(5)],
            at_least=3,
            rel=lambda val, b: b[0] <= val <= b[1]
        )
        @CoverPoint(
            f"{self.hierarchy}.Timer Enable",
            xf=lambda tr: (self.regs.read_reg_value("CTRL") & 0b1 == 0b1),
            bins=[True, False],
            bins_labels=["timer enabled" if i else "timer disabled" for i in [True, False]],
            at_least=3,
        )
        @CoverPoint(
            f"{self.hierarchy}.Timer Restart",
            xf=lambda tr: (self.regs.read_reg_value("CTRL") & 0b10 == 0b10),
            bins=[True, False],
            bins_labels=["timer restarted" if i else "timer not restarted" for i in [True, False]],
            at_least=3,
        )
        @CoverPoint(
            f"{self.hierarchy}.PWM0 Enable",
            xf=lambda tr: (self.regs.read_reg_value("CTRL") & 0b100 == 0b100),
            bins=[True, False],
            bins_labels=["pwm0 enabled" if i else "pwm0 disabled" for i in [True, False]],
            at_least=3,
        )
        @CoverPoint(
            f"{self.hierarchy}.PWM1 Enable",
            xf=lambda tr: (self.regs.read_reg_value("CTRL") & 0b1000 == 0b1000),
            bins=[True, False],
            bins_labels=["pwm1 enabled" if i else "pwm1 disabled" for i in [True, False]],
            at_least=3,
        )
        @CoverPoint(
            f"{self.hierarchy}.PWM Deadtime Enable",
            xf=lambda tr: (self.regs.read_reg_value("CTRL") & 0b10000 == 0b10000),
            bins=[True, False],
            bins_labels=["deadtime enabled" if i else "deadtime disabled" for i in [True, False]],
            at_least=3,
        )
        @CoverPoint(
            f"{self.hierarchy}.Invert PWM0",
            xf=lambda tr: (self.regs.read_reg_value("CTRL") & 0b100000 == 0b100000),
            bins=[True, False],
            bins_labels=["PWM0 output inverted" if i else "PWM0 output not inverted" for i in [True, False]],
            at_least=3,
        )
        @CoverPoint(
            f"{self.hierarchy}.Invert PWM1",
            xf=lambda tr: (self.regs.read_reg_value("CTRL") & 0b1000000 == 0b1000000),
            bins=[True, False],
            bins_labels=["PWM1 output inverted" if i else "PWM1 output not inverted" for i in [True, False]],
            at_least=3,
        )
        @CoverPoint(
            f"{self.hierarchy}.Timer Count Direction",
            xf=lambda tr: (self.regs.read_reg_value("CFG") & 0b11),
            bins=[0b10, 0b01, 0b11 ],
            bins_labels=["Up Counting", "Down Counting", "UP/Down Counting"],
            at_least=3,
        )
        @CoverPoint(
            f"{self.hierarchy}.Timer Count Periodic or One Shot",
            xf=lambda tr: (self.regs.read_reg_value("CFG") & 0b100 == 0b100),
            bins=[True, False],
            bins_labels=["Periodic Count" if i else "One Shot Count" for i in [True, False]],
            at_least=3,
        )
# # PWM0
#     # Up Count
#         # 0, 1 
#         # No action , Low
#         @CoverPoint(
#             f"{self.hierarchy}.PWM0. Up Count. No action, Low",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b10 , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 0, DownCount=False) , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 1, DownCount=False)),
#             bins=[ (True , i, j) for i in range(4) for j in range(4) if i!=j ],
#             bins_labels=[( "Up Count" , f"{i}  No action" , f"{j}  Low") for i in ["Zero", "CMPX", "CMPY", "Reload"] for j in ["Zero", "CMPX","CMPY", "Reload"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 0, 2 
#         # No action , High
#         @CoverPoint(
#             f"{self.hierarchy}.PWM0. Up Count. No action, High",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b10 , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 0, DownCount=False) , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 2, DownCount=False)),
#             bins=[ (True , i, j) for i in range(4) for j in range(4) if i!=j ],
#             bins_labels=[( "Up Count" , f"{i}  No action" , f"{j}  High") for i in ["Zero", "CMPX", "CMPY", "Reload"] for j in ["Zero", "CMPX","CMPY", "Reload"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 0, 3 
#         # No action , Invert
#         @CoverPoint(
#             f"{self.hierarchy}.PWM0. Up Count. No action, Invert",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b10 , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 0, DownCount=False) , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 3, DownCount=False)),
#             bins=[ (True , i, j) for i in range(4) for j in range(4) if i!=j ],
#             bins_labels=[( "Up Count" , f"{i}  No action" , f"{j}  Invert") for i in ["Zero", "CMPX", "CMPY", "Reload"] for j in ["Zero", "CMPX","CMPY", "Reload"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 1, 2 
#         # High , Low
#         @CoverPoint(
#             f"{self.hierarchy}.PWM0. Up Count. High, Low",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b10 , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 1, DownCount=False) , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 2, DownCount=False)),
#             bins=[ (True , i, j) for i in range(4) for j in range(4) if i!=j ],
#             bins_labels=[( "Up Count" , f"{i}  High" , f"{j}  Low") for i in ["Zero", "CMPX", "CMPY", "Reload"] for j in ["Zero", "CMPX","CMPY", "Reload"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 1, 3 
#         # High , Invert
#         @CoverPoint(
#             f"{self.hierarchy}.PWM0. Up Count. High, Invert",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b10 , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 1, DownCount=False) , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 3, DownCount=False)),
#             bins=[ (True , i, j) for i in range(4) for j in range(4) if i!=j ],
#             bins_labels=[( "Up Count" , f"{i}  High" , f"{j}  Invert") for i in ["Zero", "CMPX", "CMPY", "Reload"] for j in ["Zero", "CMPX","CMPY", "Reload"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 2, 3 
#         # Low , Invert
#         @CoverPoint(
#             f"{self.hierarchy}.PWM0. Up Count. Low, Invert",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b10 , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 2, DownCount=False) , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 3, DownCount=False)),
#             bins=[ (True , i, j) for i in range(4) for j in range(4) if i!=j ],
#             bins_labels=[( "Up Count" , f"{i}  Low" , f"{j}  Invert") for i in ["Zero", "CMPX", "CMPY", "Reload"] for j in ["Zero", "CMPX","CMPY", "Reload"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2] 
#         )

# # PWM0
#     # Down Count
#         # 0, 1 
#         # No action , Low
#         @CoverPoint(
#             f"{self.hierarchy}.PWM0. Down Count. No action, Low",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b01 , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 0, DownCount=True) , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 1, DownCount=True)),
#             bins=[ (True , i, j) for i in [0,3,4,5] for j in [0,3,4,5] if i!=j ],
#             bins_labels=[( "Down Count" , f"{i}  No action" , f"{j}  Low") for i in ["Zero", "Reload", "CMPX", "CMPY"] for j in ["Zero", "Reload", "CMPX", "CMPY"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 0, 2 
#         # No action , High
#         @CoverPoint(
#             f"{self.hierarchy}.PWM0. Down Count. No action, High",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b01 , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 0, DownCount=True) , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 2, DownCount=True)),
#             bins=[ (True , i, j) for i in [0,3,4,5] for j in [0,3,4,5] if i!=j ],
#             bins_labels=[( "Down Count" , f"{i}  No action" , f"{j}  High") for i in ["Zero", "Reload", "CMPX", "CMPY"] for j in ["Zero", "Reload", "CMPX", "CMPY"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 0, 3 
#         # No action , Invert
#         @CoverPoint(
#             f"{self.hierarchy}.PWM0. Down Count. No action, Invert",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b01 , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 0, DownCount=True) , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 3, DownCount=True)),
#             bins=[ (True , i, j) for i in [0,3,4,5] for j in [0,3,4,5] if i!=j ],
#             bins_labels=[( "Down Count" , f"{i}  No action" , f"{j}  Invert") for i in ["Zero", "Reload", "CMPX", "CMPY"] for j in ["Zero", "Reload", "CMPX", "CMPY"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 1, 2 
#         # High , Low
#         @CoverPoint(
#             f"{self.hierarchy}.PWM0. Down Count. High, Low",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b01 , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 1, DownCount=True) , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 2, DownCount=True)),
#             bins=[ (True , i, j) for i in [0,3,4,5] for j in [0,3,4,5] if i!=j ],
#             bins_labels=[( "Down Count" , f"{i}  High" , f"{j}  Low") for i in ["Zero", "Reload", "CMPX", "CMPY"] for j in ["Zero", "Reload", "CMPX", "CMPY"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 1, 3 
#         # High , Invert
#         @CoverPoint(
#             f"{self.hierarchy}.PWM0. Down Count. High, Invert",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b01 , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 1, DownCount=True) , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 3, DownCount=True)),
#             bins=[ (True , i, j) for i in [0,3,4,5] for j in [0,3,4,5] if i!=j ],
#             bins_labels=[( "Down Count" , f"{i}  High" , f"{j}  Invert") for i in ["Zero", "Reload", "CMPX", "CMPY"] for j in ["Zero", "Reload", "CMPX", "CMPY"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 2, 3 
#         # Low , Invert
#         @CoverPoint(
#             f"{self.hierarchy}.PWM0. Down Count. Low, Invert",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b01 , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 2, DownCount=True) , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), 3, DownCount=True)),
#             bins=[ (True , i, j) for i in [0,3,4,5] for j in [0,3,4,5] if i!=j ],
#             bins_labels=[( "Down Count" , f"{i}  Low" , f"{j}  Invert") for i in ["Zero", "Reload", "CMPX", "CMPY"] for j in ["Zero", "Reload", "CMPX", "CMPY"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

# # PWM1
#     # Up Count
#         # 0, 1 
#         # No action , Low
#         @CoverPoint(
#             f"{self.hierarchy}.PWM1. Up Count. No action, Low",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b10 , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 0, DownCount=False) , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 1, DownCount=False)),
#             bins=[ (True , i, j) for i in range(4) for j in range(4) if i!=j ],
#             bins_labels=[( "Up Count" , f"{i}  No action" , f"{j}  Low") for i in ["Zero", "CMPX", "CMPY", "Reload"] for j in ["Zero", "CMPX", "CMPY", "Reload"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 0, 2 
#         # No action , High
#         @CoverPoint(
#             f"{self.hierarchy}.PWM1. Up Count. No action, High",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b10 , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 0, DownCount=False) , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 2, DownCount=False)),
#             bins=[ (True , i, j) for i in range(4) for j in range(4) if i!=j ],
#             bins_labels=[( "Up Count" , f"{i}  No action" , f"{j}  High") for i in ["Zero", "CMPX", "CMPY", "Reload"] for j in ["Zero", "CMPX", "CMPY", "Reload"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 0, 3 
#         # No action , Invert
#         @CoverPoint(
#             f"{self.hierarchy}.PWM1. Up Count. No action, Invert",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b10 , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 0, DownCount=False) , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 3, DownCount=False)),
#             bins=[ (True , i, j) for i in range(4) for j in range(4) if i!=j ],
#             bins_labels=[( "Up Count" , f"{i}  No action" , f"{j}  Invert") for i in ["Zero", "CMPX", "CMPY", "Reload"] for j in ["Zero", "CMPX","CMPY", "Reload"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 1, 2 
#         # High , Low
#         @CoverPoint(
#             f"{self.hierarchy}.PWM1. Up Count. High, Low",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b10 , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 1, DownCount=False) , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 2, DownCount=False)),
#             bins=[ (True , i, j) for i in range(4) for j in range(4) if i!=j ],
#             bins_labels=[( "Up Count" , f"{i}  High" , f"{j}  Low") for i in ["Zero", "CMPX", "CMPY", "Reload"] for j in ["Zero", "CMPX","CMPY", "Reload"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 1, 3 
#         # High , Invert
#         @CoverPoint(
#             f"{self.hierarchy}.PWM1. Up Count. High, Invert",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b10 , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 1, DownCount=False) , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 3, DownCount=False)),
#             bins=[ (True , i, j) for i in range(4) for j in range(4) if i!=j ],
#             bins_labels=[( "Up Count" , f"{i}  High" , f"{j}  Invert") for i in ["Zero", "CMPX", "CMPY", "Reload"] for j in ["Zero", "CMPX","CMPY", "Reload"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 2, 3 
#         # Low , Invert
#         @CoverPoint(
#             f"{self.hierarchy}.PWM1. Up Count. Low, Invert",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b10 , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 2, DownCount=False) , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 3, DownCount=False)),
#             bins=[ (True , i, j) for i in range(4) for j in range(4) if i!=j ],
#             bins_labels=[( "Up Count" , f"{i}  Low" , f"{j}  Invert") for i in ["Zero", "CMPX", "CMPY", "Reload"] for j in ["Zero", "CMPX","CMPY", "Reload"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2] 
#         )
# # PWM1
#     # Down Count
#         # 0, 1 
#         # No action , Low
#         @CoverPoint(
#             f"{self.hierarchy}.PWM1. Down Count. No action, Low",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b01 , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 0, DownCount=True) , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 1, DownCount=True)),
#             bins=[ (True , i, j) for i in [0,3,4,5] for j in [0,3,4,5] if i!=j ],
#             bins_labels=[( "Down Count" , f"{i}  No action" , f"{j}  Low") for i in ["Zero", "Reload", "CMPX", "CMPY"] for j in ["Zero", "Reload", "CMPX", "CMPY"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 0, 2 
#         # No action , High
#         @CoverPoint(
#             f"{self.hierarchy}.PWM1. Down Count. No action, High",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b01 , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 0, DownCount=True) , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 2, DownCount=True)),
#             bins=[ (True , i, j) for i in [0,3,4,5] for j in [0,3,4,5] if i!=j ],
#             bins_labels=[( "Down Count" , f"{i}  No action" , f"{j}  High") for i in ["Zero", "Reload", "CMPX", "CMPY"] for j in ["Zero", "Reload", "CMPX", "CMPY"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 0, 3 
#         # No action , Invert
#         @CoverPoint(
#             f"{self.hierarchy}.PWM1. Down Count. No action, Invert",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b01 , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 0, DownCount=True) , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 3, DownCount=True)),
#             bins=[ (True , i, j) for i in [0,3,4,5] for j in [0,3,4,5] if i!=j ],
#             bins_labels=[( "Down Count" , f"{i}  No action" , f"{j}  Invert") for i in ["Zero", "Reload", "CMPX", "CMPY"] for j in ["Zero", "Reload", "CMPX", "CMPY"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 1, 2 
#         # High , Low
#         @CoverPoint(
#             f"{self.hierarchy}.PWM1. Down Count. High, Low",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b01 , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 1, DownCount=True) , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 2, DownCount=True)),
#             bins=[ (True , i, j) for i in [0,3,4,5] for j in [0,3,4,5] if i!=j ],
#             bins_labels=[( "Down Count" , f"{i}  High" , f"{j}  Low") for i in ["Zero", "Reload", "CMPX", "CMPY"] for j in ["Zero", "Reload", "CMPX", "CMPY"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 1, 3 
#         # High , Invert
#         @CoverPoint(
#             f"{self.hierarchy}.PWM1. Down Count. High, Invert",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b01 , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 1, DownCount=True) , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 3, DownCount=True)),
#             bins=[ (True , i, j) for i in [0,3,4,5] for j in [0,3,4,5] if i!=j ],
#             bins_labels=[( "Down Count" , f"{i}  High" , f"{j}  Invert") for i in ["Zero", "Reload", "CMPX", "CMPY"] for j in ["Zero", "Reload", "CMPX", "CMPY"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

#         # 2, 3 
#         # Low , Invert
#         @CoverPoint(
#             f"{self.hierarchy}.PWM1. Down Count. Low, Invert",
#             xf=lambda tr: ((self.regs.read_reg_value("CFG") & 0b11)==0b01 , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 2, DownCount=True) , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), 3, DownCount=True)),
#             bins=[ (True , i, j) for i in [0,3,4,5] for j in [0,3,4,5] if i!=j ],
#             bins_labels=[( "Down Count" , f"{i}  Low" , f"{j}  Invert") for i in ["Zero", "Reload", "CMPX", "CMPY"] for j in ["Zero", "Reload", "CMPX", "CMPY"] if i!=j],
#             at_least=3,
#             rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
#         )

        def sample(tr):
            uvm_info("coverage_ip", f"tr = {tr}", UVM_LOW)
        if do_sampling:
            sample(tr)

    def actions_combinations(self):
        cov_points = []
        action_labels = {
            0: "No action",
            1: "Low",
            2: "High",
            3: "Invert"
        }
        for action1 in range(4):
            for action2 in range(action1 + 1, 4):
                if (action1 != action2):
                    action1_label = action_labels[action1]
                    action2_label = action_labels[action2]
                    print(action1, action2)    
                # PWM0
                    #Up Count
                    cov_points.append(CoverPoint(
                        f"{self.hierarchy}.PWM0. Up Count.{action1_label} , {action2_label}",
                        xf=lambda tr, action1 = action1, action2 = action2: ((self.regs.read_reg_value("CFG") & 0b11)==0b10 , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), action1, DownCount=False) , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), action2, DownCount=False)),
                        bins=[ (True , i, j) for i in range(4) for j in range(4) if i!=j ],
                        bins_labels=[( "Up Count" , f"{i}  {action1_label}" , f"{j}  {action2_label}") for i in ["Zero", "CMPX", "CMPY", "Reload"] for j in ["Zero", "CMPX","CMPY", "Reload"] if i!=j],
                        # at_least=3,
                        rel=lambda val , b  : val[0]==b[0] and val[1]==b[1] and val[2]==b[2] 
                    ))
                    # Down Count
                    cov_points.append(CoverPoint(
                        f"{self.hierarchy}.PWM0. Down Count.{action1_label} , {action2_label}",
                        xf=lambda tr, action1 = action1, action2 = action2: ((self.regs.read_reg_value("CFG") & 0b11)==0b01 , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), action1, DownCount=True) , self.get_event_with_action(self.regs.read_reg_value("PWM0CFG"), action2, DownCount=True)),
                        bins=[ (True , i, j) for i in [0,3,4,5] for j in [0,3,4,5] if i!=j ],
                        bins_labels=[( "Down Count" , f"{i}  {action1_label}" , f"{j}  {action2_label}") for i in ["Zero", "Reload", "CMPX", "CMPY"] for j in ["Zero", "Reload", "CMPX", "CMPY"] if i!=j],
                        at_least=3,
                        rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
                    ))
                # PWM1
                    # Up Count 
                    cov_points.append(CoverPoint(
                        f"{self.hierarchy}.PWM1. Up Count.{action1_label} , {action2_label}",
                        xf=lambda tr, action1 = action1, action2 = action2: ((self.regs.read_reg_value("CFG") & 0b11)==0b10 , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), action1, DownCount=False) , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), action2, DownCount=False)),
                        bins=[ (True , i, j) for i in range(4) for j in range(4) if i!=j ],
                        bins_labels=[( "Up Count" , f"{i}  {action1_label}" , f"{j}  {action2_label}") for i in ["Zero", "CMPX", "CMPY", "Reload"] for j in ["Zero", "CMPX","CMPY", "Reload"] if i!=j],
                        at_least=3,
                        rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
                    ))
                    # Down Count
                    cov_points.append(CoverPoint(
                        f"{self.hierarchy}.PWM1. Down Count.{action1_label} , {action2_label}",
                        xf=lambda tr, action1 = action1, action2 = action2: ((self.regs.read_reg_value("CFG") & 0b11)==0b01 , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), action1, DownCount=True) , self.get_event_with_action(self.regs.read_reg_value("PWM1CFG"), action2, DownCount=True)),
                        bins=[ (True , i, j) for i in [0,3,4,5] for j in [0,3,4,5] if i!=j ],
                        bins_labels=[( "Down Count" , f"{i}  {action1_label}" , f"{j}  {action2_label}") for i in ["Zero", "Reload", "CMPX", "CMPY"] for j in ["Zero", "Reload", "CMPX", "CMPY"] if i!=j],
                        at_least=3,
                        rel=lambda val , b : val[0]==b[0] and val[1]==b[1] and val[2]==b[2]
                    ))
        return cov_points

    
    def get_event_with_action (self, reg, action, DownCount):
        action_list = [((reg >> i) & 0b11) for i in range (0,12,2)]
        if DownCount:
            action_list[1] = -1
            action_list[2] = -1
        try: 
            event = action_list.index(action); 
        except ValueError: 
            event = -1
        return event
    

    def apply_decorators(self, decorators):
        def decorator_wrapper(func):
            for decorator in decorators:
                func = decorator(func)
            return func
        return decorator_wrapper


        
        