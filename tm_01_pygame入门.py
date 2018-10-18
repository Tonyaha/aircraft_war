from plane_sprites import *

# 初始化 pygame ，初始化后才能使用pygame提供的其他模块，除Rect(描述矩形区域)
pg.init()

# display创建、管理窗口， set_mode()初始化窗口(480,700)窗口大小
screen = pg.display.set_mode((480, 700))

# 绘制背景图像
# 1.加载图像数据
background = pg.image.load('./images/background.png')

# 2.窗口对象调用blit() 绘制图像 >> 数据、位置(元组) 从x=0，y=0 的位置开始绘制
screen.blit(background, (0, 0))

# 3.update更新屏幕显示
#pg.display.update()

# 绘制英雄的飞机
hero = pg.image.load('./images/me1.png')
screen.blit(hero, (200, 500))
# pg.display.update()

# 可以在所有绘制工作(blit())后统一调用
pg.display.update()

# 创建时钟对象，1s执行刷新60次
clock = pg.time.Clock()

# 循环不结束 ，就不调用quit() ==> 游戏循环：游戏的正式开始，上面的部分叫做游戏的初始化
# 1. 定义rect 记录飞机的初始位置
hero_rect = pg.Rect(200,500,102,126)
print('游戏正式开始.....')



# 创建敌机的 精灵
enemy1 = GameSprite('./images/enemy1.png')
enemy1.rect = pg.Rect(0, -randint(43, 200), 57, 43)
enemy1_2 = GameSprite('./images/enemy1.png')
enemy1_2.rect = pg.Rect(80, -randint(100, 200), 57, 43)

enemy2 = GameSprite(image_name='./images/enemy2.png', speed=2)
enemy2.rect = pg.Rect(150, -randint(69, 200), 66, 69)

enemy2_2 = GameSprite(image_name='./images/enemy2.png', speed=2)
enemy2_2.rect = pg.Rect(350, -randint(100, 200), 66, 69)

# 创建敌机的 精灵组
enemy_group = pg.sprite.Group(enemy1, enemy1_2, enemy2, enemy2_2)

while True:
    # 指定循环体内部的代码执行频率
    clock.tick(60)

    # 捕获事件
    event_list = pg.event.get() # 返回当前用户所有操作的列表
    for event in event_list:
        # 判断用户是否点击了关闭按钮
        if event.type == pg.QUIT:
            print('用户点击了关闭按钮,游戏结束....')
            pg.quit()

            # 直接退出系统
            exit()

    # 2.修改飞机位置
    hero_rect.y -= 1

    # 判断飞机的位置
    if hero_rect.y == -126: # 飞机完全消失后改变位置
        hero_rect.y = 700

    # 3. 调用 blit方法绘制图像
    screen.blit(background,(0, 0)) # 消除飞机残影
    screen.blit(hero, hero_rect)



    # 让精灵组调用两个方法
    # update - 让组中所有精灵更新位置
    enemy_group.update()

    # draw - 在screen上绘制所有精灵,draw()需要知道绘制在什么对象上
    enemy_group.draw(screen)


    # 4. 调用update() 更新显示，每次调用都需要绘制一遍（背景先被绘制）
    pg.display.update()

pg.quit()
