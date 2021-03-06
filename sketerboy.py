import pygame
import random

from pygame.constants import  QUIT
from pygame.rect import *
def playsketerboy():
# pygame 초기화
    pygame.init()
    pygame.display.set_caption("MHD")
    background = pygame.image.load("img/background/background.png")

    pygame.init()
    pygame.display.set_caption("mohamD")
    pygame.mixer.music.load("mp3/sketerboy.mp3")
    pygame.mixer.music.play(-1)
# ======== 함수 ===============================
# 키 이벤트 처리하기
    def resultProcess(direction):
        global isColl, score, DrawResult, result_ticks
        if isColl and CollDirection.direction == direction:
            score += 10
            CollDirection.y = -1
            DrawResult = 1
        else:
            DrawResult = 2
        result_ticks = pygame.time.get_ticks()
    def eventProcess():
        global isActive, score, health
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isActive = False
                if health > 0:
                    if event.key == pygame.K_UP:  # 0
                        resultProcess(0)
                    if event.key == pygame.K_LEFT:  # 1
                        resultProcess(1)
                    if event.key == pygame.K_DOWN:  # 2
                        resultProcess(2)
                    if event.key == pygame.K_RIGHT:  # 3
                        resultProcess(3)
                else:
                    if event.key == pygame.K_SPACE:
                        score = 0
                        health = health_MAX
                        for direc in Directions:
                            direc.y = -1
    # 방향 아이콘 클래스
    class Direction(object):
        def __init__(self):
            self.pos = None
            self.direction = 0
            self.image = pygame.image.load(f"img/up.png")
            self.image = pygame.transform.scale(self.image, (80, 80))
            self.rotated_image = pygame.transform.rotate(self.image, 0)
            self.y = -1
            self.x = int(SCREEN_WIDTH / 2) - (self.image.get_width() / 2)

        def rotate(self, direction=0):
            self.direction = direction
            self.rotated_image = pygame.transform.rotate(
                self.image, 90 * self.direction)

        def draw(self):
            if self.y >= SCREEN_HEIGHT:
                self.y = 5
                return True
            elif self.y == -1:
                return False
            else:
                self.y += 1
                self.pos = screen.blit(self.rotated_image, (self.x, self.y))
                return False

        ###################################################################################
        # 방향 아이콘 생성과 그리기
    def drawIcon():
        global start_ticks, health
        if health <= 0:
            return

        elapsed_time = (pygame.time.get_ticks() - start_ticks)
        if elapsed_time > 700:
            start_ticks = pygame.time.get_ticks()
            for direc in Directions:
                if direc.y == -1:
                    direc.y = 100
                    direc.rotate(direction=random.randint(0, 3))
                    break

        for direc in Directions:
            if direc.draw():
                health -= 1

###################################################################################
# 타겟 영역 그리기와 충돌 확인하기
    def draw_targetArea():
        global isColl, CollDirection
        isColl = False
        for direc in Directions:
            if direc.y == -1:
                continue
            if direc.pos.colliderect(targetArea):
                isColl = True
                CollDirection = direc
                pygame.draw.rect(screen, (255, 255, 255, 0.3), targetArea)
                break
        pygame.draw.rect(screen, (0, 0, 0), targetArea, 3)

        ###################################################################################
        # 문자 넣기
    def setText():
        global score, health
        mFont = pygame.font.SysFont("굴림", 40)

        mtext = mFont.render(f'score : {score}', True, 'black')
        screen.blit(mtext, (138, 10, 0, 0))

        mtext = mFont.render(f'health : {health}', True, 'black')
        screen.blit(mtext, (125, 42, 0, 0))

        if health <= 0:
            mFont = pygame.font.SysFont("굴림", 90)
            mtext = mFont.render(f'Game over!!', True, 'red')
            tRec = mtext.get_rect()
            tRec.centerx = SCREEN_WIDTH / 2
            tRec.centery = SCREEN_HEIGHT / 2 - 40
            pygame.mixer.music.pause()
            screen.blit(mtext, tRec)
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
        ###################################################################################
        # 결과 이모티콘 그리기ㅇㅇ
    def drawResult():
        global DrawResult, result_ticks
        if result_ticks > 0:
            elapsed_time = (pygame.time.get_ticks() - result_ticks)
            if elapsed_time > 400:
                result_ticks = 0
                DrawResult = 0
        screen.blit(resultImg[DrawResult], resultImgRec)
    ###################################################################################
    # ========= 변수 =================================
    isActive = True
    global isColl
    global health
    global SCREEN_WIDTH
    SCREEN_WIDTH = 400
    global SCREEN_HEIGHT
    SCREEN_HEIGHT = 600
    global health_MAX
    health_MAX = 5
    global score
    score = 0
    health = health_MAX
    isColl = False
    global CollDirection
    CollDirection = 0
    global DrawResult, result_ticks
    DrawResult, result_ticks = 0, 0
    global start_ticks
    start_ticks = pygame.time.get_ticks()
    global clock
    clock = pygame.time.Clock()
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    global i
    # 방향 아이콘==>여기 i 문제있음
    Directions = [Direction() for i in range(0, 10)]
    # 타겟 박스
    targetArea = Rect(SCREEN_WIDTH/3, 500, SCREEN_WIDTH /3, 50)
    # 결과 이모티콘
    resultFileNames = ["img/good.png", "img/perfect.png", "img/bad.png"]
    resultImg = []
    for i, name in enumerate(resultFileNames):
        resultImg.append(pygame.image.load(name))
        resultImg[i] = pygame.transform.scale(resultImg[i], (150, 75))

    resultImgRec = resultImg[0].get_rect()
    resultImgRec.centerx = SCREEN_WIDTH / 2.15 - resultImgRec.width / 2 - 40 #아이콘과 박스 width 정렬
    resultImgRec.centery = targetArea.centery

    # ========= 반복문 ===============================
    while (isActive):
            screen.blit(background,(0, 0))
            eventProcess()
            # Directions[0].y = 100
            # Directions[0].rotate(0)
            # Directions[0].draw()
            draw_targetArea()
            drawIcon()
            setText()
            drawResult()
            pygame.display.update()
            clock.tick(400)
#################################################################################
if __name__ == '__main__':
    playsketerboy()