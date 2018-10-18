import random# 官方模块
import pygame as pg # 第三方模块

# 屏幕大小的常量
SCREEN_RECT = pg.Rect(0, 0, 480, 700)

# 刷新的帧率
FRAME_PER_SEC = 60

# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pg.USEREVENT

# 英雄发送子弹事件
HERO_FIRE_EVENT = pg.USEREVENT + 1

# 大型飞机生命值
BIG_ENEMY_MAX_LIFE = 50

# 中型飞机生命值
MID_ENEMY_MAX_LIFE = 20


class GameSprite(pg.sprite.Sprite):
    ''' 飞机大战游戏 精灵 '''
    def __init__(self, image_name = None, speed = 1):
        # 调用父类的初始化方法，否则无法使用父类提供的属性、方法
        super().__init__()

        # 定义对象的属性
        self.image = pg.image.load(image_name).convert_alpha() # 加载图片
        self.rect = self.image.get_rect() # 得到图片的数据,默认x=0,y=0
        self.speed = speed # 移动速度

        # 检测非透明部分是否发生碰撞，碰撞时指定pg.sprite.collide_mask
        self.mask = pg.mask.from_surface(self.image)

        # 敌机坠毁图片列表索引
        self.index = 0

    def update(self, *args):

        # 在垂直方向移动
        self.rect.y += self.speed


class Background(GameSprite):
    '''游戏背景精灵'''
    def __init__(self, is_alt=False):
        # 1.调用父类方法实现精灵的创建（image、rect、speed）
        super().__init__('./images/background.png')

        # 2. 判断是否是交替图像，如果是(True)，需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self, *args):

        # 1.调用父类的方法实现
        super().update()

        # 2.判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class EnemySmall(GameSprite):
    '''敌机精灵'''
    def __init__(self):

        # 1.调用父类初始话方法(不调用就不能使用父类提供的属性、方法)，创建敌机精灵，同时指定敌机图片
        super().__init__('./images/enemy1.png')

        self.down_enemy_images = [pg.image.load('./images/enemy1_down1.png').convert_alpha(),
                                      pg.image.load('./images/enemy1_down2.png').convert_alpha(),
                                      pg.image.load('./images/enemy1_down3.png').convert_alpha(),
                                      pg.image.load('./images/enemy1_down4.png').convert_alpha()]

        # 2.指定敌机的初始速度
        self.speed = random.randint(2, 3)

        # 3.指定敌机的初始随机位置
        self.rect.x = random.randint(0, SCREEN_RECT.width-self.rect.width)

        # pygame.Rect提供的bottom属性，bottom = y + height
        self.rect.bottom = 0

        self.energy = 1

    def update(self, *args):

        # 1.调用父类的方法，保持垂直方向的飞行
        super().update()

        # 2.判断敌机是否移出屏幕，如果是，则销毁敌机对象（从精灵组删除精灵）
        if self.rect.y >= SCREEN_RECT.height:
            # print('飞机飞出屏幕，从精灵组中删除敌机')

            # kill()可以将精灵从精灵组中删除，并且从内存中销毁(销毁前调用__del__)
            self.kill()

    def __del__(self):
        print('小型 敌机挂了 %s ' % self.rect)


class EnemyMid(GameSprite):

    def __init__(self):
        super().__init__('./images/enemy2.png', random.randint(1, 2))
        self.down_enemy_images = [pg.image.load('./images/enemy2_down1.png').convert_alpha(),
                                      pg.image.load('./images/enemy2_down2.png').convert_alpha(),
                                      pg.image.load('./images/enemy2_down3.png').convert_alpha(),
                                      pg.image.load('./images/enemy2_down4.png').convert_alpha()]
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        self.rect.bottom = -5 * SCREEN_RECT.height
        # 检测非透明部分是否发生碰撞，碰撞时指定pg.sprite.collide_mask
        self.mask = pg.mask.from_surface(self.image)

        # 血槽最大值
        self.energy = MID_ENEMY_MAX_LIFE

    def update(self, *args):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            # print('飞机飞出屏幕，从精灵组中删除敌机')

            # kill()可以将精灵从精灵组中删除，并且从内存中销毁(销毁前调用__del__)
            self.kill()
    def __del__(self):
        print('中型 敌机挂了......')


class EnemyBig(GameSprite):

    def __init__(self):
        super().__init__('./images/enemy3_n1.png', 1)
        self.image1 = pg.image.load('./images/enemy3_n1.png').convert_alpha()
        self.image2 = pg.image.load('./images/enemy3_n2.png').convert_alpha()
        self.down_enemy_images = [pg.image.load('./images/enemy3_down1.png').convert_alpha(),
                                      pg.image.load('./images/enemy3_down2.png').convert_alpha(),
                                      pg.image.load('./images/enemy3_down3.png').convert_alpha(),
                                      pg.image.load('./images/enemy3_down4.png').convert_alpha(),
                                      pg.image.load('./images/enemy3_down5.png').convert_alpha(),
                                      pg.image.load('./images/enemy3_down6.png').convert_alpha()]

        # 3.指定敌机的初始随机位置
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        self.rect.bottom = -10 * SCREEN_RECT.height

        # 检测非透明部分是否发生碰撞，碰撞时指定pg.sprite.collide_mask
        self.mask = pg.mask.from_surface(self.image)

        # 血槽最大值
        self.energy = BIG_ENEMY_MAX_LIFE

    def update(self, *args):
        super().update()
        # 2.判断敌机是否移出屏幕，如果是，则销毁敌机对象（从精灵组删除精灵）
        if self.rect.y >= SCREEN_RECT.height:
            # print('飞机飞出屏幕，从精灵组中删除敌机')

            # kill()可以将精灵从精灵组中删除，并且从内存中销毁(销毁前调用__del__)
            self.kill()

    def __del__(self):
        print('大型 敌机挂了 %s ' % self.rect)


class Hero(GameSprite):
    '''英雄精灵'''

    # 英雄命的条数
    hero_lives = 3

    def __init__(self):
        # 1.调用父类初始话方法(不调用就不能使用父类提供的属性、方法)，设置image、速度
        super().__init__('./images/me1.png', 0)

        # 必须定义两张图片才能切换，？？
        self.image1 = pg.image.load('./images/me1.png').convert_alpha()
        self.image2 = pg.image.load('./images/me2.png').convert_alpha()

        # 英雄撞毁图片
        self.down_hero_images = []
        self.down_hero_images.extend([pg.image.load('./images/me_destroy_1.png').convert_alpha(), pg.image.load('./images/me_destroy_2.png').convert_alpha(),
                                 pg.image.load('./images/me_destroy_3.png').convert_alpha(), pg.image.load('./images/me_destroy_4.png').convert_alpha()])

        # 2.英雄初始位置， bottom = y + height
        # self.rect.x, self.rect.bottom = (SCREEN_RECT.width - self.rect.width)/2, SCREEN_RECT.height-80
        self.rect.centerx, self.rect.bottom = SCREEN_RECT.centerx, SCREEN_RECT.height-50

        # 3.创建子弹精灵组,再在主程序中的update_sprites()设置
        self.bullets_group = pg.sprite.Group()

    def update(self, *args):

        # 英雄水平方向移动
        self.rect.x += self.speed

        # 控制英雄不能离开屏幕
        if self.rect.x <= -self.rect.width//2:
            self.rect.x = -self.rect.width//2
        elif self.rect.right >= SCREEN_RECT.right + self.rect.width//2:
            # right = x + width
            self.rect.right = SCREEN_RECT.right + self.rect.width//2

    def fire(self):
        # print('发射子弹....')
        list_x = [1.22, 2, 5]
        list_y = [70, self.rect.height, 70]
        for i in (0, 1, 2):
            # 1.创建子弹精灵
            bullet = Bullet()

            # 2.设置精灵位置
            bullet.rect.bottom = self.rect.bottom - list_y[i]
            bullet.rect.centerx = self.rect.right - (self.rect.width // list_x[i])

            # 3.将精灵添加到精灵组
            self.bullets_group.add(bullet)


class Bullet(GameSprite):
    ''' 子弹精灵类 '''

    def __init__(self):
        # 1. 调用父类方法，设置子弹图片、速度
        super().__init__(random.choice(['./images/bullet1.png', './images/bullet2.png']), -10)

    def update(self, *args):
        # 1.调用父类方法，让子弹沿垂直方向飞行
        super().update()

        # 2.判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        # print('子弹被销毁....')
        pass


class NumberOfLife(GameSprite):
    def __init__(self):
        super().__init__('./images/life.png', 0)
        self.rect.x = SCREEN_RECT.left + 5
        self.rect.bottom = SCREEN_RECT.height - 5
