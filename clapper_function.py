import random as r
from copy import deepcopy
import clapper_class as CC
from colorama import Fore, Style

def color(string,temp_color):
    '''赋予字符串颜色
    
    获取原字符串和颜色,返回带有颜色属性的字符串'''
    colors = {"BLACK": Fore.BLACK,
              "RED": Fore.RED,
              "GREEN": Fore.GREEN,
              "YELLOW": Fore.YELLOW,
              "BLUE": Fore.BLUE,
              "MAGENTA": Fore.MAGENTA,
              "CYAN": Fore.CYAN,
              "WHITE": Fore.WHITE,
    }
    string = colors[temp_color] + string + Style.RESET_ALL
    return string

#各种策略
Cultivate = CC.Strategy(1,color('修养','GREEN'),0,1,0,0,0,0,0,0)
'''关于策略1.[修养](Cultivate)的属性
    自身[能量] +1'''

Attack = CC.Strategy(2,color('攻击','RED'),0,-1,0,-1,0,0,1,0)
'''关于策略2.[攻击](Attack)的属性
    能被敌方的[闪避]躲过,造成 1 点伤害'''

Dodge = CC.Strategy(3,color('闪避','BLUE'),0,0,0,0,0,0,0,1)
'''关于策略3.[闪避](Dodge)的属性
    闪避敌方[攻击]'''

Slash = CC.Strategy(4,color('斩杀','RED'),0,-5,3,-2,0,0,2,0.5)
'''关于策略4.[斩杀](Slash)的属性
    无视敌方的[闪避],造成 2 点伤害'''

Defense = CC.Strategy(5,color('防御','BLUE'),0,-1,0,0,0,0,0,2)
'''关于策略5.[防御](Defense)的属性
    防御敌方[斩杀]'''

Pray = CC.Strategy(6,color('祈祷','GREEN'),1,-4,10,0,0,0,0,0)
'''关于策略6.[祈祷](Pray)的属性
    [生命] +1 ,[暴击率] + 10%~13%'''

Confess = CC.Strategy(6,color('忏悔','CYAN'),0,-4,15,0,0,0,0,0)
'''关于策略7.[忏悔](Confess)的属性
    *只有[祈祷]3次时,才会激发
    [生命]有概率 -1,且概率为 [暴击率]/1.2
    [暴击率] + 15%~20%'''

def individual_strategy_list():
    '''返回策略表副本
    
    '''
    temp_strategy_list = [0,deepcopy(Cultivate),deepcopy(Attack),
                          deepcopy(Dodge),deepcopy(Slash),
                          deepcopy(Defense),deepcopy(Pray)]
    return temp_strategy_list

def computer_decision(computer,player):
    '''电脑进行决策
    
    根据双方情况作出判断'''
    while True: 
      if computer.strategy_list[6].name == Pray.name and computer.strategy_list[6].times == 3:
         computer.strategy_list[6] = deepcopy(Confess)
      computer.strategy = r.choice(computer.strategy_list[1:])
      if player.energy >= 5:
        if r.random() <= 0.6:
          computer.strategy = Defense 
      elif computer.strategy == Defense:
         continue
      #若玩家[能量] > = 5,将有 60% 的概率采取[防御]。否则不采取[防御]
      if computer.energy + computer.strategy.energy_O >= 0:
        computer.strategy_times(strategy_times_add = 1)
        break

def player_decision(player):
    while True:
      for i in range(1,len(player.strategy_list)):
        print(f"{i}.{player.strategy_list[i].name}",end = '\t')
      P_temp_strategy = input("\n请选择你的策略: ")
      if P_temp_strategy in [str(i) for i in range(1,len(player.strategy_list))]:
        player.strategy = player.strategy_list[int(P_temp_strategy)]
        if player.energy + player.strategy.energy_O < 0:
          print("\n能量不足,请重新决策!")
        if player.energy + player.strategy.energy_O >= 0:
          player.strategy_times(strategy_times_add = 1)
          break
    pass
    

def outcome(individual_one,individual_two):
    '''判断胜负情况
      
    玩家胜为 1,电脑胜为 2,否则保持 -1'''
    if individual_one.HP <= 0:
      individual_two.win_game += 1
      print("恭喜您胜利了！",end = '')
      return 1         #玩家胜利情况
    elif individual_two.HP <= 0:
      individual_one.win_game += 1
      print("大败而归！",end = '')
      return 2          #电脑胜利情况
    else:
      return -1

def round_end_init(individual_one,individual_two):
    '''一局结束后进行结算
   
    '''
    print(f"\n{individual_one.name} 选择了 [{individual_one.strategy.name}]\t{individual_one.description}")
    print("")
    print(f"{individual_two.name} 选择了 [{individual_two.strategy.name}]\t\t{individual_two.description}")
    print("------------------------------------------------------------------------")
    individual_one.description_init()
    individual_two.description_init()
    for i in (individual_one,individual_two):
       if i.strategy_list[6].name == Pray.name and i.strategy_list[6].times == 3:
          i.strategy_list[6] = deepcopy(Confess)
    #打印决策结果、判断胜负、回合数 +1

def is_critical(critical_rate):
    '''判断是否造成暴击
   
    输入[暴击率],返回bool值'''
    if r.random()*100 <= critical_rate:
      return True
    else:
      return False
