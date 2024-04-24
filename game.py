import random
import pygame
import time
import string

pygame.init()
WIDTH = 1400
HEIGHT = 750
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("pai-gow game")
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 80)


class Card:
    def __init__(self, name, cost, sell, type, attack, health):
        self.name = name
        self.cost = cost
        self.sell = sell
        self.type = type
        if type == 'slow' or 'guy' or 'passive' or 'land':
            self.speed = 0
        else:
            self.speed = 1
        if type == 'guy':
            self.attack = attack
            self.health = health
        else:
            self.attack = None
            self.health = None


class Create_Deck_Handler():
    def __init__(self, deck):
        self.deck = deck
        self.myfont = pygame.font.Font('freesansbold.ttf', 30)
        self.piles = [[] for _ in range(5)]
        self.boxes,self.texts,self.locs = self.draw_cards()
        self.pile_images = self.draw_piles()
        self.inside_piles = [[] for _ in range(5)]

    def draw_cards(self):
        card_boxes = [None for _ in range(15)]
        card_texts = [None for _ in range(15)]
        card_text_loc = [[] for _ in range(15)]
        for i in range(0, 7):
            card_boxes[i] = pygame.Rect(160 * i + 250, 10, 150, 150)
            card_texts[i] = self.myfont.render(f'{self.deck[i].name}', True, 'black')
            card_text_loc[i] = [160*i+253, 10]
        for i in range(7, 15):
            card_boxes[i] = pygame.Rect(160 * (i - 7), 210, 150, 150)
            card_texts[i] = self.myfont.render(f'{self.deck[i].name}', True, 'black')
            card_text_loc[i] = [160 * (i-7) + 3, 210]
        return card_boxes, card_texts, card_text_loc

    def change_loc(self, card, start, finish, start_image, finish_image):
        add_card = start.pop(card)
        finish.append(add_card)
        card_image = start_image.pop(card)
        finish_image.append(card_image)

    # def insert_pile(self, card, pile):
    #     add_card = self.deck.pop(card)
    #     self.piles[pile].append(add_card)
    #
    # def change_pile(self, card, pile_add, pile_remove):
    #     add_card = self.piles[pile_remove].pop(card)
    #     self.piles[pile_add].append(add_card)
    #
    # def insert_deck(self, card, pile_remove):
    #     add_card = self.piles[pile_remove].pop(card)
    #     self.deck.append(add_card)

    def draw_piles(self):
        ps = [None for _ in range(5)]
        for i in range(5):
            ps[i] = pygame.Rect(250 * i + 50, 500, 200, 200)
            # for j, card in enumerate(self.piles[i]):
            #     pygame.draw.rect(screen, 'white', [250 * i + 55, 500 - j * 20, 150, 150])
        return ps


def gen_rand_word():
    length = random.choice(range(10))
    output = ""
    for _ in range(length):
        output += random.choice(string.ascii_lowercase)
    return output


start_cards = [Card(gen_rand_word(), 0, 0, 'guy', 0, 0) for _ in range(60)]
shop_deck = [n for n in range(500)]  # each will be filled with cards
shop = [0 for _ in range(5)]

deck1 = [0 for _ in range(15)]  # will be arrays of cards
deck2 = [0 for _ in range(15)]
state = 'start'


def draw_game(handler):
    buttons_list = []
    if state == 'start':
        start = pygame.draw.rect(screen, 'white', [600, 300, 300, 100], 0, 5)
        start_text = font.render('START', True, 'black')
        screen.blit(start_text, (630, 300))
        buttons_list.append(start)
    if state == 'create_decks':
        for i in range(5):
            pygame.draw.rect(screen, 'blue', handler.pile_images[i])
            for card in handler.inside_piles[i]:
                pygame.draw.rect(screen, 'white', card)
        for i in range(15):
            pygame.draw.rect(screen, 'white', handler.boxes[i])
            screen.blit(handler.texts[i], handler.locs[i])
        # NOTE not using deck2 because that would be a second player
        # figure out how to get a second player's perspective
        deck_text = font.render("Deck:", True, 'white')
        screen.blit(deck_text, (0, 50))
    if state == 'select_stack':
        pass
    if state == 'game_board':
        pass
    if state == 'brief_shop':
        pass
    if state == 'keep_sell':
        pass
    if state == 'shop_phase':
        pass
    return buttons_list


# main game loop
active_box = None
cur_handler = None
run = True
while run:
    timer.tick(fps)
    screen.fill('black')

    buttons = draw_game(cur_handler)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if state == 'start':
            if event.type == pygame.MOUSEBUTTONUP:
                if buttons[0].collidepoint(event.pos):
                    random.shuffle(start_cards)
                    for i in range(0, 15):
                        deck1[i] = start_cards[i]
                        deck2[i] = start_cards[i + 15]
                    cur_handler = Create_Deck_Handler(deck1)
                    state = 'create_decks'
        if state == 'create_decks':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if active_box is None:
                    for i in range(15):
                        if cur_handler.boxes[i].collidepoint(event.pos):
                            active_box = i
            if event.type == pygame.MOUSEMOTION:
                if active_box is not None:
                    cur_handler.boxes[active_box].move_ip(event.rel)
                    cur_handler.locs[active_box][0] += event.rel[0]
                    cur_handler.locs[active_box][1] += event.rel[1]
            if event.type == pygame.MOUSEBUTTONUP:
                if active_box is not None:
                    for i in range(5):
                        if active_box is not None:
                            if cur_handler.pile_images[i].colliderect(cur_handler.boxes[active_box]):
                                x, y = cur_handler.pile_images[i].left, cur_handler.pile_images[i].top
                                cur_handler.change_loc(active_box,cur_handler.deck,cur_handler.piles[i])
                                # cur_handler.boxes[active_box].clamp_ip(cur_handler.pile_images[i])
                                cur_handler.boxes[active_box].update(x+5,y+20*len(cur_handler.piles[i]),150,150)
                                cur_handler.locs[active_box] = [x+5,y+20*len(cur_handler.piles[i])]
                                active_box = None


    pygame.display.flip()
pygame.quit()
