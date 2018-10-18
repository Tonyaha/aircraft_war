from plane_sprites import *


class PlaneGame(object):
    '''飞机大战主游戏类'''

    def __init__(self):
        print('游戏初始化....')
        # 1.创建游戏窗口
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_RECT.size)
        pg.display.set_caption('飞机大战')

        # 2.创建游戏时钟
        self.clock = pg.time.Clock()

        # 3.调用私有方法，精灵和精灵组的创建
        self.__create_sprites()

        # 4.设置定时器事件（从pygame.event.get()中获取事件） - 创建敌机， 1s 创建一次
        pg.time.set_timer(CREATE_ENEMY_EVENT, 1000)

        # 5.英雄发射子弹事件,0.5s
        pg.time.set_timer(HERO_FIRE_EVENT, 150)

        # 用于延迟
        self.delay = 100

        # 用于切换图片
        self.flag_switch_image = False

        # 英雄是否和敌机相撞
        self.flag_hero_enemy_collide = False

        # 背景音乐
        pg.mixer.init()
        pg.mixer_music.load('./music/bg_music_2.mp3')
        pg.mixer_music.play(-1)
        pg.mixer_music.set_volume(0.2)

        # 音效
        self.bullet = pg.mixer.Sound('./music/bullet.wav')
        self.bullet.set_volume(0.1)
        self.bomb = pg.mixer.Sound('./music/bomb.wav')
        self.bomb.set_volume(0.1)

        # 统计得分
        self.score = 0
        self.score_font = pg.font.SysFont('arial', 35)

        # 颜色
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        # 血条颜色
        self.energy_color = self.BLACK

    def __create_sprites(self):

        # 创建背景精灵
        bg1 = Background()
        bg2 = Background(True)

        # 创建精灵组,将精灵添加到精灵组
        self.background_group = pg.sprite.Group(bg1, bg2)

        # 创建敌机精灵组
        self.enemy_small_group = pg.sprite.Group()
        self.enemy_mid_group = pg.sprite.Group()
        self.enemy_big_group = pg.sprite.Group()

        # 创建英雄精灵组,因为英雄在其他位置会使用,所以单独定义成属性
        self.hero = Hero()
        self.hero_group = pg.sprite.Group(self.hero)

        # 存放子弹被撞击的敌机
        self.add_small_enemy_group = pg.sprite.Group()
        self.add_mid_enemy_group = pg.sprite.Group()
        self.add_big_enemy_group = pg.sprite.Group()

        # 剩余生命数量
        self.number_of_life_group = pg.sprite.Group()
        for i in range(3):
            life = NumberOfLife()
            life.rect.x += i*life.rect.width
            self.number_of_life_group.add(life)

    def start_game(self):
        print('....游戏开始....')
        # 游戏循环 -- 游戏正式开始，之前的都是为开始做准备
        while True:
            # 1.设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)

            # 2.事件监听
            self.__event_handler()

            # 3.碰撞检测
            self.__check_collide()

            # 4. 更新、绘制精灵组
            self.__update_sprites()

            # 得分显示
            score_text = self.score_font.render('Score : %s' % str(self.score), True, self.WHITE)
            self.screen.blit(score_text, (10, 5))

            # 5.更新显示
            pg.display.update()

            # 用于切换图片
            if not (self.delay % 5):
                # 每循环5次执行一次
                self.flag_switch_image = not self.flag_switch_image

            #  用于延迟
            self.delay -= 1
            if not self.delay:
                # 此时 delay=0
                self.delay = 100

    def __event_handler(self):

        for event in pg.event.get():
            # 判断是否点击关闭按钮
            if event.type == pg.QUIT:
                print('\n用户点击了关闭按钮....')
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT: # 定时器 - 每隔1000ms创建一架敌机
                # print('敌机出场.....')
                # 1.创建敌机精灵
                enemy = EnemySmall()

                # 2.将精灵添加到精灵组
                self.enemy_small_group.add(enemy)

                if not (self.delay % 10):
                    enemy_mid = EnemyMid()
                    self.enemy_mid_group.add(enemy_mid)
                elif not (self.delay % 12):
                    enemy_big = EnemyBig()
                    self.enemy_big_group.add(enemy_big)
            elif event.type == HERO_FIRE_EVENT:
                if not self.flag_hero_enemy_collide:
                    self.hero.fire()

            # elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
            #     print('向右移动....')

        # 使用键盘模块提供的方法获取按键 -- 监听英雄移动
        keys_pressed = pg.key.get_pressed()

        if self.flag_hero_enemy_collide:
            self.hero.speed = 0
        else:
            # 判断元组中对应按键索引值 1
            if keys_pressed[pg.K_RIGHT]:
                # print('向右移动...')
                # if self.hero.rect.x >= SCREEN_RECT.rect.width - self.hero.width:
                #     return
                self.hero.speed = 10
            elif keys_pressed[pg.K_LEFT]:
                self.hero.speed = -10
            else:
                self.hero.speed = 0

    def __collide_bullet_enemy_group(self, enemy_group, add_to_group):
        # 1.子弹摧毁敌机 ,pg.sprite.collide_mask结合 self.mask = pg.mask.from_surface(self.image)检测非透明部分是否发生碰撞，
        group_enemies = pg.sprite.groupcollide(enemy_group, self.hero.bullets_group, False, True)
        for enemy in group_enemies:
            if enemy.energy == 0:
                add_to_group.add(enemy)
                enemy_group.remove(enemy)
            enemy.energy -= 1

    def __collide_hero_enemy_group(self, enemy_group):
        # 2.敌机撞毁精灵,返回一个列表
        enemies = pg.sprite.spritecollide(self.hero, enemy_group, False, pg.sprite.collide_mask)

        # 判断列表是否有内容
        if len(enemies) > 0:
            for enemy in enemies:
                enemy.speed = 0
                if not (self.delay % 5):
                    if not enemy.index:
                        self.bomb.play()
                        self.flag_hero_enemy_collide = True
                        self.flag_num_of_life = True
                    self.hero.image = self.hero.down_hero_images[self.hero.index]
                    enemy.image = enemy.down_enemy_images[enemy.index]

                    enemy.index = (enemy.index + 1) % len(enemy.down_enemy_images)
                    self.hero.index = (self.hero.index + 1) % len(self.hero.down_hero_images)
                    if not enemy.index:
                        self.hero.kill()
                        enemy.kill()

                        # 英雄每牺牲一次，命数减一
                        Hero.hero_lives -= 1
                        if Hero.hero_lives == 0:
                            print('英雄牺牲了....')
                            # 结束游戏
                            PlaneGame.__game_over()
                        self.hero = Hero()
                        self.hero_group.add(self.hero)
                        self.flag_hero_enemy_collide = False

    # 碰撞检测
    def __check_collide(self):
        self.__collide_bullet_enemy_group(self.enemy_small_group, self.add_small_enemy_group)
        self.__collide_bullet_enemy_group(self.enemy_mid_group, self.add_mid_enemy_group)
        self.__collide_bullet_enemy_group(self.enemy_big_group, self.add_big_enemy_group)

        self.__collide_hero_enemy_group(self.enemy_small_group)
        self.__collide_hero_enemy_group(self.enemy_mid_group)
        self.__collide_hero_enemy_group(self.enemy_big_group)

    def __update_sprites(self):
        '''
            让精灵组调用两个方法
            update - 让组中所有精灵更新位置
            draw - 在screen上绘制所有精灵,draw()需要知道绘制在什么对象上
        '''

        # 背景精灵组
        self.background_group.update()
        self.background_group.draw(self.screen)

        # 敌机精灵组 , 先更新位置，再绘制，否则会出现时快时慢的情况
        self.enemy_big_group.update()
        self.__draw_lines(self.enemy_big_group, BIG_ENEMY_MAX_LIFE)

        self.enemy_mid_group.update()
        self.__draw_lines(self.enemy_mid_group, MID_ENEMY_MAX_LIFE)

        self.enemy_small_group.update()
        self.enemy_small_group.draw(self.screen)

        # 被子弹撞爆炸的敌机
        if self.add_small_enemy_group:
            if not (self.delay % 3):
                self.__collide_effect(self.add_small_enemy_group, 0)
        elif self.add_mid_enemy_group:
            if not (self.delay % 3):
                self.__collide_effect(self.add_mid_enemy_group, 1)
        elif self.add_big_enemy_group:
            if not (self.delay % 3):
                self.__collide_effect(self.add_big_enemy_group, 2)

        # 绘制剩余生命数
        self.number_of_life_group.update()
        if self.hero.hero_lives > 0:
            if self.flag_hero_enemy_collide:
                count = 0
                for life in self.number_of_life_group:
                    if count == self.hero.hero_lives - 1:
                        self.number_of_life_group.remove(life)
                    count += 1
            self.number_of_life_group.draw(self.screen)

        # 英雄精灵组 更新、绘制
        self.hero_group.update()
        if not self.flag_hero_enemy_collide:
            if self.flag_switch_image:
                self.hero.image = self.hero.image1
            else:
                self.hero.image = self.hero.image2
        self.hero_group.draw(self.screen)

        # 子弹精灵组
        self.hero.bullets_group.update()
        self.hero.bullets_group.draw(self.screen)

    @staticmethod
    def __game_over():
        print('....游戏结束....')

        # 卸载所有模块
        pg.quit()

        # 直接退出
        exit()

    # 被子弹撞击效果
    def __collide_effect(self, group, flag=0):
        for e in group:
            if e.index == 0:
                self.bomb.play()
                e.speed = 0
            e.image = e.down_enemy_images[e.index]
            group.draw(self.screen)

            e.index = (e.index + 1) % len(e.down_enemy_images)
            if e.index == 0:
                e.kill()
                if flag == 0:
                    self.score += 1000
                elif flag == 1:
                    self.score += 6000
                elif flag == 2:
                    self.score += 10000

    # 绘制血槽
    def __draw_lines(self, group, total_life):
        for e in group:
            pg.draw.line(self.screen, self.BLACK, (e.rect.left, e.rect.top - 5),
                         (e.rect.left + e.rect.width, e.rect.top - 5), 4)
            if e.energy / total_life >= 0.2:
                self.energy_color = self.GREEN
            else:
                self.energy_color = self.RED
            pg.draw.line(self.screen, self.energy_color, (e.rect.left, e.rect.top - 5),
                    (e.rect.left + e.rect.width * (e.energy / total_life), e.rect.top - 5), 4)
            if not (total_life - BIG_ENEMY_MAX_LIFE):
                if self.flag_switch_image:
                    e.image = e.image1
                else:
                    e.image = e.image2
        group.draw(self.screen)


if __name__ == '__main__':
    play = PlaneGame()
    play.start_game()
