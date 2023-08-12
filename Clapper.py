import os
import clapper_class as CC
import clapper_function as CF
from colorama import init,Style

# 启用自动重置颜色功能
init(autoreset=True)
if __name__ == '__main__':
    exit = ''    #标记是否退出游戏
    game,round = 1,1     #局数、回合数
    flag = -1   #标记结果
    COMPUTER = CC.Individual("Com",0)
    CHARACTER = [0,CC.Individual("",0),CC.Individual("TEST",0)]
    print(f"1.人机对战\n2.上帝模式")
    mode = input("请选择模式:")
    PLAYER = CHARACTER[int(mode)]
    if mode == '1':
      PLAYER.name = input("请输入玩家名称: ")
    while  exit != 'q':
      while exit != 'q' and flag < 0:
        print(f"第{game}局 || 第{round}回合")
        print(f"玩家\t生命\t能量\t暴击率\t胜率")
        COMPUTER.panel()
        PLAYER.panel()
        pass
        #打印游戏面板
        if mode == '1':
          CF.player_decision(PLAYER)
        elif mode == '2':
          CF.computer_decision(PLAYER,COMPUTER)
        #玩家进行决策
        CF.computer_decision(COMPUTER,PLAYER)
        #电脑进行决策

        COMPUTER.effect(PLAYER)
        PLAYER.effect(COMPUTER)
        if mode == '1':
          os.system('cls')     #清屏,仅保留一局结果
        CF.round_end_init(COMPUTER,PLAYER)
        flag = CF.outcome(COMPUTER,PLAYER)
        round += 1
        pass

      COMPUTER.init(game)       
      PLAYER.init(game)
      round = 1
      flag = -1
      game +=1
      #一局结束，进行初始化、局数+1
      exit = input("再来一局吗？(输入 q 退出游戏):")
      #判断是否再来一局
    pass



    
