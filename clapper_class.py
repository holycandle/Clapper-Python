import random as r
from colorama import init, Fore, Style



# 启用自动重置颜色功能
init(autoreset=True)

class Strategy:
    '''各种可采用的决策
    
    各种决策的效益'''
    def __init__(self , number , name , 
                 HP_O , energy_O , critical_O ,
                 HP_E , energy_E , critical_E ,
                 level_A = 0 , level_D = 0 ,
                 times = 0):
      self.name = name
      self.number = number
      self.HP_O = HP_O
      self.energy_O = energy_O
      self.critical_O = critical_O
      self.HP_E = HP_E
      self.energy_E = energy_E
      self.critical_E = critical_E
      self.level_A = level_A
      self.level_D = level_D
      self.times = times

import clapper_function as CF
class Individual:
    '''个体属性
    
    默认为HP为3,能量为0,暴击率为0,胜率为0,'''
    def __init__(self,name,
                 win_game , HP = 5 , energy = 0 , critical = 0 ,
                 win_per = 0.00 , strategy = None ,strategy_list = None,
                 description = ""):
        self.name = name
        self.win_game = win_game
        self.HP = HP
        self.energy = energy
        self.critical = critical
        self.win_per = win_per
        self.strategy = strategy
        if strategy_list is None:
           strategy_list = CF.individual_strategy_list()
        self.strategy_list = strategy_list
        self.description = description

    def panel(self):
        '''打印面板
        
        显示个体名称、生命、能量、暴击率、胜率'''
        print(f"{self.name}\t",end = "")
        for i in range(self.HP):
            print(Fore.RED + "+",end = "")
        print(f"\t{self.energy}\t{self.critical}%\t{self.win_per}%")

    def strategy_times(self,temp_strategy = None,strategy_times_add = 0):
        '''调用个体的决策统计表，返回、增加相应决策的统计数

        输入要查询的决策(默认为正在采取的决策),需要增加的数目(默认为 0)'''
        if temp_strategy is None:
          temp_strategy = self.strategy
        self.strategy_list[temp_strategy.number].times += strategy_times_add
        return self.strategy_list[temp_strategy.number].times

    def effect(self,individual_E):  
        '''根据双方决策分别造成影响
        
        需输入敌人、决策情况'''
        feature = {'名称': CF.color('名称','WHITE'),
                   '胜利局数': CF.color('胜利局数','WHITE'),
                   '生命': CF.color('生命','RED'),
                   '能量': CF.color('能量','GREEN'),
                   '暴击率': CF.color('暴击率','RED'),
                   '胜率': CF.color('胜率','WHITE'),
                   '策略': CF.color('策略','WHITE'),
                   '描述': CF.color('描述','WHITE')
        }

        is_hurt =  self.strategy.level_A > max(individual_E.strategy.level_D,individual_E.strategy.level_A)
        final_HP_O = self.strategy.HP_O
        final_energy_O = self.strategy.energy_O
        final_critical_O = self.strategy.critical_O
        final_HP_E = self.strategy.HP_E
        final_energy_E = self.strategy.energy_E
        final_critical_E = self.strategy.critical_E

        if self.strategy.name == CF.Slash.name:          
        #当自身采取[斩杀]时,有[暴击率]加成
          if is_hurt:
            final_critical_O += r.randint(4,7)    #若[斩杀]造成伤害,加成为 7%~10%(基础为 3% , 修正为 4%~7%)
          else:
            final_critical_O += r.randint(0,2)    #若未造成伤害,加成为 3%~5%(基础为 3% , 修正为 0%~2%)
            self.description += f",可惜被[{individual_E.strategy_list[5].name}]抵挡住了!"
            print(f" [{feature['暴击率']}] + {final_critical_O}%")

        elif self.strategy.name == CF.Pray.name:          
        #当自身采取[祈祷]时,有[暴击率]加成  
            final_critical_O += r.randint(0,3)    #[暴击率]加成为10%~13%(基础为 10%,修正为 0%~3%)           

        elif self.strategy.name == CF.Confess.name:
        #当自身采取[忏悔],有[生命]-1风险,有[暴击率]加成
            final_HP_O += -1 if r.random() < self.critical/120 else 0   #[生命]-1,概率为[暴击率]/1.2
            final_critical_O += r.randint(0,5)            #[暴击率]加成为15%~20%(基础为 15%,修正为 0%~5%)
        if not(self.strategy.HP_E < 0 and is_hurt) :
        #当双方策略不同,且自身攻击等级大于敌方防御等级和攻击等级时，才能造成伤害
          final_HP_E = 0
        
        if self.critical == 100:
        #[暴击率]封顶,不再增加
           final_critical_O = 0

        if self.strategy.HP_E < 0 and is_hurt and CF.is_critical(self.critical):
        #[暴击]判定成功,造成2倍伤害
          final_HP_E *=2   
          self.description += f",造成了 {abs(final_HP_E)} 点伤害的暴击！"
        

        pass
        #确定最终决策效益

        self.HP += final_HP_O
        if final_HP_O != 0:
           self.description += f" , [{feature['生命']}] + {final_HP_O}"

        self.energy += final_energy_O
        if final_energy_O > 0:
           self.description += f" , [{feature['能量']}] + {final_energy_O}"

        self.critical += final_critical_O
        if self.critical > 100:
           self.critical = 100
        if final_critical_O != 0:
           self.description += f" , [{feature['暴击率']}] + {final_critical_O}%"
        
        individual_E.HP += final_HP_E
        
        individual_E.energy += final_energy_E
        
        individual_E.critical += final_critical_E

    def description_init(self):
        '''仅初始化[描述]
       
        '''
        self.description = self.description.replace(self.description,"") 
    
    def init(self,game):
        '''初始化
        
        属性归零,计算胜率'''
        self.__init__(self.name,self.win_game)
        self.win_per = round(100*self.win_game/game,2)  #计算胜率
        self.description_init()  #描述初始化
        if self.strategy_list[6].name == '祈祷' and self.strategy_list[6].times == 3:
           self.strategy_list[6] == CF.Confess
    pass
