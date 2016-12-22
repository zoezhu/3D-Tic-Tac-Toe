__author__ = "Zoe ZHU"
__copyright__ = "Copyright 2016, Pitt"

import numpy as np
import random
from copy import deepcopy


def create_win_condition():
    win_condition = np.zeros((76, 4, 3))
    initial_idx = 0
    create_tree(1, initial_idx, [1, 2, 0], win_condition)
    initial_idx = 16
    create_tree(1, initial_idx, [0, 1, 2], win_condition)
    initial_idx = 32
    create_tree(1, initial_idx, [2, 0, 1], win_condition)
    initial_idx = 48
    create_tree(2, initial_idx, [0, 1, 2], win_condition)
    initial_idx = 56
    create_tree(2, initial_idx, [2, 1, 0], win_condition)
    initial_idx = 64
    create_tree(2, initial_idx, [1, 2, 0], win_condition)
    initial_idx = 72
    create_tree(3, initial_idx, [0, 1, 2], win_condition)

    return win_condition.tolist()


def create_tree(treeType, initial_idx, order, win_condition):
    temp = np.zeros(3,dtype=np.int)
    if treeType == 1:
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    idx = initial_idx + i * 4 + j
                    temp[order[0]] = i
                    temp[order[1]] = j
                    temp[order[2]] = k
                    win_condition[idx][k] = temp
    elif treeType == 2:
        for i in range(4):
            for j in range(4):
                idx = initial_idx + i
                temp[order[0]] = i
                temp[order[1]] = j
                temp[order[2]] = j
                win_condition[idx][j] = temp

                idx = initial_idx + i + 4
                temp[order[2]] = 3 - j
                win_condition[idx][j] = temp
    else:
        for i in range(4):
            idx = initial_idx
            temp[order[0]] = i
            temp[order[1]] = i
            temp[order[2]] = i
            win_condition[idx][i] = temp

            idx = initial_idx + 1
            temp[order[1]] = 3 - i
            temp[order[2]] = 3 - i
            win_condition[idx][i] = temp

            idx = initial_idx + 2
            temp[order[1]] = i
            temp[order[2]] = 3 - i
            win_condition[idx][i] = temp

            idx = initial_idx + 3
            temp[order[1]] = 3 - i
            temp[order[2]] = i
            win_condition[idx][i] = temp


def record_new_play(new_play,satisfy,satisfy_2,win_condition,win_condition_2):
    initial_idx = 0
    is_win = record_tree(1, initial_idx, [1, 2, 0], new_play, win_condition, win_condition_2, satisfy, satisfy_2)
    if is_win:
        return True
    initial_idx = 16
    is_win = record_tree(1, initial_idx, [0, 1, 2], new_play, win_condition, win_condition_2, satisfy, satisfy_2)
    if is_win:
        return True
    initial_idx = 32
    is_win = record_tree(1, initial_idx, [2, 0, 1], new_play, win_condition, win_condition_2, satisfy, satisfy_2)
    if is_win:
        return True
    initial_idx = 48
    is_win = record_tree(2, initial_idx, [0, 1, 2], new_play, win_condition, win_condition_2, satisfy, satisfy_2)
    if is_win:
        return True
    initial_idx = 56
    is_win = record_tree(2, initial_idx, [2, 1, 0], new_play, win_condition, win_condition_2, satisfy, satisfy_2)
    if is_win:
        return True
    initial_idx = 64
    is_win = record_tree(2, initial_idx, [1, 2, 0], new_play, win_condition, win_condition_2, satisfy, satisfy_2)
    if is_win:
        return True
    initial_idx = 72
    is_win = record_tree(3, initial_idx, [0, 1, 2], new_play, win_condition, win_condition_2, satisfy, satisfy_2)
    if is_win:
        return True
    initial_idx = 73
    is_win = record_tree(4, initial_idx, [0, 1, 2], new_play, win_condition, win_condition_2, satisfy, satisfy_2)
    if is_win:
        return True
    initial_idx = 74
    is_win = record_tree(4, initial_idx, [2, 1, 0], new_play, win_condition, win_condition_2, satisfy, satisfy_2)
    if is_win:
        return True
    initial_idx = 75
    is_win = record_tree(4, initial_idx, [1, 0, 2], new_play, win_condition, win_condition_2, satisfy, satisfy_2)
    if is_win:
        return True

    return False


def record_tree(treeType,initial_idx,order,new_play,win_condition,win_condition_2,satisfy,satisfy_2):
    idx = 0
    if treeType == 1:
        for i in range(2):
            idx += new_play[order[i]] * (4**(1-i))
    elif treeType == 2:
        if new_play[order[1]]==new_play[order[2]]:
            idx = new_play[order[0]]
        elif new_play[order[1]]+new_play[order[2]]==3:
            idx = new_play[order[0]] + 4
        else:
            return False
    elif treeType == 3:
        if new_play[order[0]]==new_play[order[1]] and new_play[order[0]]==new_play[order[2]]:
            idx = 0
        else:
            return False
    else:
        if new_play[order[1]]+new_play[order[2]]==3 and new_play[order[1]]==new_play[order[2]]:
            idx = 0
        else:
            return False


    win_condition_2[int(initial_idx + idx)] = []
    for i in satisfy_2:
        if int(initial_idx + idx) in i:
            i.remove(int(initial_idx + idx))
            break

    condition = 4 - len(win_condition[int(initial_idx + idx)])
    if condition == 4:
        return False
    if condition == 0:
        satisfy[0].append(int(initial_idx+idx))
    elif condition == 1:
        satisfy[0].remove(int(initial_idx+idx))
        satisfy[1].append(int(initial_idx+idx))
    elif condition == 2:
        satisfy[1].remove(int(initial_idx+idx))
        satisfy[2].append(int(initial_idx+idx))
    else:
        return True

    win_condition[int(initial_idx + idx)].remove(new_play)
    return False


def find_condition(satisfy_n, win_condition,checkerboard):
    if len(satisfy_n) == 0:
        return None
    for i in satisfy_n:
        for j in win_condition[i]:
            if check_play_valid(checkerboard,j,2):
                return j
    return None


def ai_next(checkerboard,satisfy_p1,satisfy_p2,win_condition_p1,win_condition_p2):
    next_step = find_condition(satisfy_p2[2],win_condition_p2,checkerboard)
    if not next_step:
        next_step = find_condition(satisfy_p1[2],win_condition_p1,checkerboard)
    else:
        checkerboard[int(next_step[0]), int(next_step[1]), int(next_step[2])] = 2
        print("AI step: ", end="")
        print([int(x + 1) for x in next_step])
        return True
    if not next_step:
        next_step = find_condition(satisfy_p2[1],win_condition_p2,checkerboard)
        if not next_step:
            next_step = find_condition(satisfy_p2[0],win_condition_p2,checkerboard)
            if not next_step:
                while True:
                    next_step = [random.randint(0, 3) for i in range(3)]
                    if check_play_valid(checkerboard,next_step,2):
                        break
    next_step = [int(x) for x in next_step]
    print("AI step: ",end="")
    print([x+1 for x in next_step])
    record_new_play(next_step,satisfy_p2,satisfy_p1,win_condition_p2,win_condition_p1)


# #test
#     print(satisfy_p2)
#     for i in satisfy_p2:
#         for j in i:
#             print(j)
#             print(win_condition_p2[j])
#             print()

    checkerboard[int(next_step[0]), int(next_step[1]), int(next_step[2])] = 2
    return False


def check_play_valid(checkerboard,next_step,sign):
    if checkerboard[int(next_step[0]),int(next_step[1]),int(next_step[2])] == 0:
        checkerboard[int(next_step[0]), int(next_step[1]), int(next_step[2])] = int(sign)
        return True
    else:
        return False



def print_checkerboard(checkerboard):
    print("(X-person, O-computer)")
    for i in range(4):
        print("-- LAYER ",end="")
        print(i+1,end="")
        print(" --")
        for j in range(4):
            for k in range(4):
                if checkerboard[i][j][k] == 0:
                    print(" . ",end="")
                elif checkerboard[i][j][k] == 1:
                    print(" X ",end="")
                else:
                    print(" O ",end="")
            print()
        print()


def main_tic_tac_toe():
    checkerboard = np.zeros((4,4,4),dtype=np.int)
    win_condition_p1 = create_win_condition()
    win_condition_p2 = deepcopy(win_condition_p1)
    satisfy_p1 = [[] for i in range(3)]
    satisfy_p2 = [[] for i in range(3)]
    step_count = 0
    who_first = input("Input who first, 0-compuer, 1-human.\n")
    if not int(who_first):
        ai_next(checkerboard,satisfy_p1,satisfy_p2,win_condition_p1,win_condition_p2)
        print_checkerboard(checkerboard)
        step_count += 1
    while True:
        if step_count == 64:
            print("****** Tie. ******")
            break
        while True:
            try:
                new_play = input("It's your turn. Input format: d,d,d\n")
                new_play = new_play.split(",")
                new_play = [int(x)-1 for x in new_play]
                if check_play_valid(checkerboard,new_play,1):
                    break
            except:
                print("Your input is incorrect, maybe the location is already taken, or maybe the format is wrong.")
                continue
        if record_new_play(new_play,satisfy_p1,satisfy_p2,win_condition_p1,win_condition_p2):
            print_checkerboard(checkerboard)
            print("****** Congratulation! You win! ******")
            break
        step_count += 1
        print_checkerboard(checkerboard)

        if step_count == 64:
            print("****** Tie. ******")
            break
        if ai_next(checkerboard,satisfy_p1,satisfy_p2,win_condition_p1,win_condition_p2):
            print_checkerboard(checkerboard)
            print("****** Sorry, you lose. ******")
            break
        print_checkerboard(checkerboard)
        step_count += 1



main_tic_tac_toe()