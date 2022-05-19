# ◆ ♠ ♥ ♣ / A 2 3 4 5 6 7 8 9 10 J Q K joker(black,color) 54장
# A◆
import random


class Card:  # 색, 모양, 숫자
    attack_card = {'A': 3, '2': 2, 'black': 5, 'color': 7}
    special_card = {'7': 77, 'J': 15, 'K': 17}  # Q 빠짐

    def __init__(self, shape, number):  # 모양이랑 숫자를 받음
        self.shape = shape  # 모양
        self.number = number  # 숫자
        self.attack = None  # 공격효과
        self.special = None  # 특수효과
        if self.number in self.attack_card:
            self.attack = self.attack_card[number]
        if self.number in self.special_card:
            self.special = self.special_card[number]
        if shape == '♠' or shape == '♣' or shape == "black":  # 색 정하기
            self.color = "black"
        else:
            self.color = "color"

    def __str__(self):
        return f"{self.shape}{self.number}"

    def __repr__(self):
        return f"{self.shape}{self.number}"


class Player:  # 플레이어한테 카드 분배
    # 카드 내기
    def __init__(self, cards):  # 각 플레이어에게 카드 분배
        self.cards = cards

    def return_possible_card(self, upper):  # 자신의 턴일 때 낼 수 있는 카드 리스트 리턴
        possible_card = []
        for i in range(len(self.cards)):  # 맨위에 있는 카드와 같은 모양 혹은 숫자 그리고 색이 있을 경우 낼 수 있는 카드 출력
            if self.cards[i].number == "joker":  # 손에 조커가 있을 때
                if upper.color == self.cards[i].color:
                    possible_card.append(self.cards[i])
            elif upper.number == "joker":  # 바닥에 조커가 있을 때
                if upper.color == self.cards[i].color:
                    possible_card.append(self.cards[i])
            elif upper.shape == self.cards[i].shape or upper.number == self.cards[i].number:  # 조커가 아닐 때
                possible_card.append(self.cards[i])
        return possible_card

    def return_attack_possible_card(self, upper):  # 낼 수 있는 공격카드 리스트를 리턴해줌
        attack_possible_card = []
        for i in range(len(self.cards)):
            if self.cards[i].attack is not None and self.cards[i].attack >= upper.attack:  # 낼 수 있는 카드 확인
                attack_possible_card.append(self.cards[i])
        return attack_possible_card

    def return_shield_possible_card(self, upper):  # 방어카드 리스트 리턴해줌
        shield_possible_card = None
        for i in range(len(self.cards)):  # 모양이 같으면서 숫자가 3이여야 함
            if self.cards[i].number == '3' and (upper.number == 'A' or upper.number == '2'):
                if self.cards[i].shape == upper.shape:
                    shield_possible_card = self.cards[i]
        return shield_possible_card

    def print(self):
        for i in self.cards:
            print(i)


class User(Player):  # 플레이어 카드 내기
    def put_card(self, possible_put_card):
        print(f"낼 수 있는 카드 : {possible_put_card}")
        print("카드 한장 먹고 싶으면 100을 입력 하세요")
        while True:
            my_put_card = int(input("낼 카드를 입력 해주세요 : ")) - 1
            if my_put_card == 99:  # 100 입력시 한장 먹기
                self.cards += draw_card(1)
                return COM_TURN
            if my_put_card >= len(self.cards):
                print("다시 입력 하세요")
                continue
            else:  # 낸 카드 손에서 빼서 위에 쌓기
                for i in range(len(self.cards)):
                    accrue_card.append(self.cards.pop(my_put_card))
                    if self.cards[i].shape == possible_put_card[my_put_card].shape and \
                            self.cards[i].number == possible_put_card[my_put_card].number:
                        accrue_card.append(self.cards.pop(i))
                        return COM_TURN


class Computer(Player):  # 컴퓨터 랜덤 카드 내기
    def put_card(self, possible_put_card):  # 컴퓨터 카드 내기
        if len(possible_put_card) == 1:  # 낼 수 있는 카드 한장 일때
            accrue_card.append(self.cards.pop(0))
            return MY_TURN
        elif len(possible_put_card) == 0:  # 낼 수 있는 카드 없을 때
            self.cards += draw_card(1)
        else:  # 낼 수 있는 카드가 2장 이상일 때
            com_put_card = random.randint(0, len(self.cards) - 1)
            for i in range(len(self.cards)):
                if self.cards[i].shape == possible_put_card[com_put_card].shape and \
                        self.cards[i].number == possible_put_card[com_put_card].number:
                    accrue_card.append(self.cards.pop(i))
                    print(f"컴퓨터가 낸 카드 : {accrue_card[-1]}")
            return MY_TURN


accrue_card = []  # 게임 진행 중 플레이어가 카드를 냄으로 누적되는 카드
card = [Card('joker', 'black'), Card('joker', 'color')]  # 게임 시작 초기 덱
my_self = User([])  # 내 카드
computer = Computer([])  # 컴퓨터 카드
MY_TURN = 1
COM_TURN = 0
turn = random.randint(0, 1)
effect_dic = {'A': 3, '2': 2, '3': 0, '7': 77, 'J': 15, 'Q': 16, 'K': 17, 'black': 5, 'color': 7}  # 공격카드 판단
decision = 0  # 카드몇장인지  결정함
special = 0  # 특수 카드 턴 바꿈


def make_card():  # 카드 만들기
    print("게임을 시작합니다!")
    shape = ('◆', '♠', '♥', '♣')
    num = ('A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K')
    num = tuple(map(str, num))
    for i in shape:
        for j in num:
            card.append(Card(i, j))  # Card 클래스로 넘겨줌
    random.shuffle(card)  # 카드 섞기
    accrue_card.append(card.pop(0))
    global my_self, computer
    my_self = User(draw_card(5))  # 시작 카드 분배
    computer = Computer(draw_card(5))  # 시작 카드 분배


def show_top_card():  # 맨 위의 카드 보여주기
    print(f"맨 위에 있는 카드 : {accrue_card[-1]}")


def draw_card(count):  # 카드 먹이기
    new_list = []
    for i in range(count):
        new_list.append(card.pop(0))
    return new_list


def start_turn(player):  # 턴 시작
    global decision
    if is_attack_situation():
        attack_card = player.return_attack_possible_card(accrue_card[-1])
        shield_card = player.return_shield_possible_card(accrue_card[-1])
        if len(attack_card) > 0 and len(shield_card) > 0:
            if turn == MY_TURN:
                choice = int(input("1번 공격, 2번 방어 : "))
            else:
                choice = random.randint(1, 2)
            if choice == 1:  # 공격
                player.put_card(attack_card)
                add_attack_card(accrue_card[-1])
            elif choice == 2:  # 방어
                player.put_card(shield_card)
                decision = 0
        elif len(attack_card) > 0:  # 공격
            player.put_card(attack_card)
            add_attack_card(accrue_card[-1])
        elif len(shield_card) > 0:  # 방어
            player.put_card(shield_card)
            decision = 0
        else:  # 공격X 방어X 쌓인 만큼 먹기
            player.cards += draw_card(decision)
            decision = 0
    else:  # 공격받는 상황이 아님
        available_card = player.return_possible_card(accrue_card[-1])
        if len(available_card) == 0:  # 낼 카드 없음
            player.cards += draw_card(decision)
            return
        player.put_card(available_card)  # 카드 냄
        if is_special_card(accrue_card[-1]):  # 맨 위의 카드가 특수카드임
            if accrue_card[-1].number == '7':  # 일시적으로 모양 바꾸기
                pass
            else:  # J, K 일 떄
                if accrue_card[-1].number == 'K':  # 한 번 더함
                    available_card = player.return_possible_card(accrue_card[-1])
                    player.put_card(available_card)
                elif accrue_card[-1].number == 'J':  # <1 : 1 기준> 한 번 더함
                    available_card = player.return_possible_card(accrue_card[-1])
                    player.put_card(available_card)
                elif accrue_card[-1].number == 'Q':  # 턴 거꾸로 돌림
                    pass
        else:  # 특수카드가 아님
            if accrue_card[-1].attack is not None:  # 낸 카드가 공격카드 일 때
                add_attack_card(accrue_card[-1])  #  decision 장 수 추가 -> 턴 넘기기
            else:  # 공격카드가 아님 : 일반 카드
                    # 턴 넘기기


def add_attack_card(top_card):  # 공격카드 장 수 더함
    global decision
    if top_card.attack is not None:
        decision = decision + top_card.attack
    else:
        return -1


def is_special_card(top_card):  # 특수카드 판단
    global special, turn
    if top_card.special is not None:
        return True
    else:
        return False


def is_attack_situation():  # 공격 상황 확인
    if decision > 0:  # 공격 받는 상황
        return True
    else:  # 공격받는 상황이 아님
        return False


def end_game():  # 게임 종료 조건 만들기
    if len(my_self.cards) == 0 or len(computer.cards) >= 20:
        print("승리하였습니다!")
        exit(1)
    elif len(my_self.cards) >= 20 or len(computer.cards) == 0:
        print("컴퓨터가 승리하였습니다!")
        exit(1)


make_card()
while True:  # 게임 진행 : 반복되는 함수들
    show_top_card()
    if turn == MY_TURN:
        print("당신의 턴 입니다")
        print(f"내가 먹어야 하는 카드 장 수 : {decision}")
        print("내 카드")
        my_self.print()
        start_turn(my_self)
    elif turn == COM_TURN:
        print("컴퓨터의 턴 입니다")
        print(f"컴퓨터가 먹어야 하는 카드 장 수 : {decision}")
        print(f"컴퓨터가 가지고 있는 카드 장 수 : {len(computer.cards)}")
        start_turn(computer)
    print("----------------------------------------------------------------------------")
    end_game()
