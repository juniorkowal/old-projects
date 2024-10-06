from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
from ursina.shaders import lit_with_shadows_shader

app=Ursina()

m=0
fish_amount=5
game_timer=120

def input(key):
    if key=='escape':
        app.userExit()

def update():
    global fish_amount
    global m
    global game_timer

    if player.life<0:
        app.userExit()
    if game_timer<0:
        app.userExit()
    if fish_amount==0:
        app.userExit()

    if player.intersects(fish_graphics).hit:
        player.caught_fish=True
        fish_graphics.position=Vec3(400,fish_graphics.y,0)

    if player.x/20==3 and player.z/20==4 and player.caught_fish:
        spawn_fish()
        for i in range(5):
            melt_floes()
        if fish_amount>0:
            fish_ui[fish_amount-1].icon='assets/fish_ui.png'
            fish_amount-=1
        player.caught_fish=False    

    if int(fish_graphics.x/20)!=20 and not floe_graphics[int(fish_graphics.x/20)][int(fish_graphics.z/20)]:
        spawn_fish()

    fish_graphics.rotation_y+=90*time.dt

    m=m+1
    num_frame=200
    n=m%num_frame
    if n<num_frame//2:
        fish_graphics.y+=time.dt
    else:
        fish_graphics.y-=time.dt

    time_frames=60
    t=m%time_frames
    if t==0 and player.start:
        game_timer-=1
        time_graphics.text=str(game_timer)

    if player.ground:
        if not (0<=int(player.x/20)<7 and 0<=int(player.z/20)<7) or not floe_graphics[int(player.x/20)][int(player.z/20)]:
            invoke(no_floe)


def melt_floes():
    pos_xz=(random.randint(0,6),random.randint(0,6))
    if not floe_graphics[pos_xz[0]][pos_xz[1]] or pos_xz==(3,4) or floe_graphics[pos_xz[0]][pos_xz[1]].melting:
        melt_floes()
    else:
        floe_graphics[pos_xz[0]][pos_xz[1]].melting=True

def spawn_fish():
    pos_xz=(random.randint(0,6),random.randint(0,6))
    if not floe_graphics[pos_xz[0]][pos_xz[1]] or pos_xz==(3,4):
        spawn_fish()
    else:
        fish_graphics.position=Vec3(pos_xz[0]*20,fish_graphics.y,pos_xz[1]*20)

def no_floe():
    player.position=Vec3(60,7.4,80)
    player.rotation_y=180
    player.life-=1
    life_graphics.text=str(player.life)
    if player.caught_fish:
        player.caught_fish=False
        spawn_fish()


class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.ground=True
        self.life=3

        camera.z=-40
        camera.y=20
        camera.rotation=(10,0,0)

        self.start=False
        self.caught_fish=False
        self.fish=Entity(parent=self,model='assets/fish.obj',texture='fish.png',scale=1,position=Vec3(self.x,self.y+0.1,self.z+0.9),shader=lit_with_shadows_shader,alpha=0,rotation_y=90)

        for key, value in kwargs.items():
            setattr(self, key ,value)

    def update(self):
        camera.x=self.x
        camera.z=self.z-60
        if self.caught_fish:
            self.fish.alpha=1
        else:
            self.fish.alpha=0

    def input(self,key):
        if self.ground and self.start:
            if key == 'd':
                self.animate_x(self.x+20, 1, resolution=int(10//time.dt), curve=curve.linear)
                self.rotation_y=90
                invoke(self.jump)
            if key == 'a':
                self.animate_x(self.x-20, 1, resolution=int(10//time.dt), curve=curve.linear)
                self.rotation_y=-90
                invoke(self.jump)
            if key == 'w':
                self.animate_z(self.z+20, 1, resolution=int(10//time.dt), curve=curve.linear)
                self.rotation_y=0
                invoke(self.jump)
            if key == 's':
                self.animate_z(self.z-20, 1, resolution=int(10//time.dt), curve=curve.linear)
                self.rotation_y=180
                invoke(self.jump)
        
    def jump(self):
        jump_sound=Audio('assets/jump.mp3', pitch=1)
        jump_sound.play()
        self.ground=False
        self.animate_y(18, 1.7, resolution=int(10//time.dt), curve=curve.out_circ)
        invoke(self.fall,delay=0.3)
        invoke(self.on_ground,delay=1)

    def fall(self):
        self.animate_y(7.4, 0.7, resolution=int(10//time.dt), curve=curve.in_circ)

    def on_ground(self):
        self.ground=True


class Floe(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.melting=False

        for key, value in kwargs.items():
            setattr(self, key ,value)

    def update(self):
        if self.melting:
            self.scale_x-=time.dt*(0.05)
            self.scale_z-=time.dt*(0.05)
        if self.scale<=0:
            destroy(self)

pivot=Entity()
sun=DirectionalLight(parent=pivot,y=2, z=3, shadows=True, rotation=(45, -45, 45))

sky = Entity(model="sphere",texture='assets/niebo.png',scale=9999,texture_scale=(10,10),double_sided=True,shader=lit_with_shadows_shader)

floe_graphics=[[0 for i in range(7)] for j in range(7)]

fish_ui=[0 for i in range(fish_amount)]

for i in range(fish_amount):
    fish_ui[i]=Button(icon='assets/fish_ui_transparent.png',scale=(0.1,0.1),position=(-5.4-0.1*i,-0.45),alpha=0,disabled=True)


fish_graphics=Entity(model='assets/fish.obj',texture='fish.png',scale=2,collider='sphere',position=Vec3(random.randint(0,6)*20,4.5,random.randint(0,6)*20),shader=lit_with_shadows_shader)

for i in range(7):
    for j in range(7):
        if i==3 and j==4:
            floe_graphics[i][j]=Floe(model='assets/igloo.obj',texture='igloo.png',collider='box',scale=(3,3,3),position=Vec3(20*i,5,20*j),rotation_y=-150,shader=lit_with_shadows_shader)
        else:
            floe_graphics[i][j]=Floe(model='assets/floe.obj',texture='floe.png',collider='box',scale=3,position=Vec3(20*i,5,20*j),rotation_y=random.randint(0,180),shader=lit_with_shadows_shader)

ground=Entity(model='plane',color=color.rgb(0,89,179),scale=10000,position=Vec3(0,-50,0),shader=lit_with_shadows_shader)

water=Entity(model='plane',texture='assets/water.png',texture_scale=(166,166),scale=2500,position=Vec3(0,4.5,0),alpha=0.3,shader=lit_with_shadows_shader)

player=Player(model='assets/player.obj',texture='assets/player.png',collider='sphere',scale=2,position=Vec3(60,7.4,0),shader=lit_with_shadows_shader)

wife=Entity(model='assets/wife.obj',texture='player.png',scale=2,position=Vec3(52,7.4,80),rotation_y=160,shader=lit_with_shadows_shader)
bow=Entity(model='assets/bow.obj',color=color.pink,scale=2,position=Vec3(52,7.4,80),rotation_y=160,shader=lit_with_shadows_shader)
roller=Entity(model='assets/roller.obj',color=color.brown,scale=2,position=Vec3(52,7.4,80),rotation_y=160,shader=lit_with_shadows_shader)


ui_background= Button(icon='assets/background.png',scale=(3,1.5),color=color.white,position=(-.15,.25),z=.1,pressed_color=color.white)

ui_tutorial= Button(icon='assets/tutorial.png',scale=(3,1.5),color=color.white,position=(-5.15,.25),z=.2,pressed_color=color.white)

start_button = Button(text='Start', highlight_color=color.blue,scale=(0.2,0.1),text_color=color.black,color=color.white,position=(0,.3))
tutorial_button = Button(text='Instrukcja', highlight_color=color.blue,scale=(0.2,0.1),text_color=color.black,color=color.white,position=(0,.15))
exit_button = Button(text='Wyjscie', highlight_color=color.blue,scale=(0.2,0.1),text_color=color.black,color=color.white,position=(0,0))

life_graphics = Button(disabled=True,text=str(3),scale=(0.2,0.1),text_color=color.black,color=color.white,position=(5.7,.4))
time_graphics = Button(disabled=True,text=str(120),scale=(0.2,0.1),text_color=color.black,color=color.white,position=(-5.7,.4))

ok_button = Button(highlight_color=color.blue,text='Ok!',scale=(0.2,0.1),text_color=color.black,color=color.white,position=(5,-.4))

def game_start():
    ui_background.x=5
    start_button.x=5
    tutorial_button.x=5
    exit_button.x=5
    life_graphics.x-=5
    time_graphics.x+=5
    destroy(ui_tutorial)
    for i in range(fish_amount):
        fish_ui[i].x+=5
    player.start=True

def tutorial_gui():
    start_button.x=5
    exit_button.x=5
    tutorial_button.x=5
    ui_background.x=5
    ui_tutorial.x+=5
    ok_button.x-=5

def ok_gui():
    start_button.x-=5
    exit_button.x-=5
    tutorial_button.x-=5    
    ui_background.x-=5
    ui_tutorial.x-=5
    ok_button.x+=5

def exit_gui():
    player.life=-1

tutorial_button.on_click=tutorial_gui
ok_button.on_click=ok_gui
start_button.on_click=game_start
exit_button.on_click=exit_gui

app.run()