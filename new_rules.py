min_ut_straight_bet = (L * (1 - ticket_price)) - (ticket_price * (1 - L))
min_ut_reverse_bet = (U * (-(1 - ticket_price))) + (ticket_price * (1 - U))
min_ut_hold = -penalty
# Computation of minimum utilities
max_ut_straight_bet = (U * (1 - ticket_price)) - (ticket_price * (1 - U))
max_ut_reverse_bet = (L * (-(1 - ticket_price))) + (ticket_price * (1 - L))
max_ut_hold = -penalty
# Computation of maximum utilities

#Maximin Rule

# Condition 1 (Choice = Buy)
if (min_ut_straight_bet > min_ut_reverse_bet) and (min_ut_straight_bet > min_ut_hold):
    buy = 1
    count_rand_1 += 1

# Condition 2 (Choice = Reverse Buy)
if (min_ut_reverse_bet > min_ut_straight_bet) and (min_ut_reverse_bet > min_ut_hold):
    rev_buy = 1
    count_rand_2 += 1

# Condition 3 (Choice = Hold)
if (min_ut_hold > min_ut_straight_bet) and (min_ut_hold > min_ut_reverse_bet):
    hold = 1
    count_rand_3 += 1

check_1 = buy + rev_buy + hold

if check_1 == 0:

    # Condition 4 (Choice = Rand(Buy; Reverse Buy))
    if (min_ut_straight_bet == min_ut_reverse_bet) and (min_ut_straight_bet != min_ut_hold):
        rand_token = random.randint(0, 1)
        if rand_token == 0:
            buy = 1
        else:
            rev_buy = 1
        count_rand_4 += 1

    # Condition 5 (Choice = Rand(Reverse Buy; Hold))
    if (min_ut_reverse_bet == min_ut_hold) and (min_ut_reverse_bet != min_ut_straight_bet):
        rand_token = random.randint(0, 1)
        if rand_token == 0:
            rev_buy = 1
        else:
            hold = 1
        count_rand_4 += 1

    # Condition 6 (Choice = Rand(Buy; Hold))
    if (min_ut_hold == min_ut_straight_bet) and (min_ut_hold != min_ut_reverse_bet):
        rand_token = random.randint(0, 1)
        if rand_token == 0:
            hold = 1
        else:
            buy = 1
        count_rand_4 += 1


check_2 = buy + rev_buy + hold

# Condition 7 (Choice = Rand(Buy; Reverse Buy; Hold))
if check_2 == 0:
    rand_token = random.randint(0, 2)
    if rand_token == 0:
        buy = 1
    if rand_token == 1:
        rev_buy = 1
    if rand_token == 2:
        hold = 1
    count_rand_7 += 1

#Hurwitz Criterion

buy_hm = alpha*min_ut_straight_bet + (1-alpha)*max_ut_straight_bet
rev_buy_hm = alpha*min_ut_reverse_bet + (1-alpha)*max_ut_reverse_bet
hold_hm = 1
#Hurwitz Meausures
#Note that hold_hm == 1, since min_ut_hold == max_ut_hold

# Condition 1 (Choice = Buy)
if (buy_hm > rev_buy_hm) and (buy_hm > hold_hm):
    buy = 1
    count_rand_1 += 1

# Condition 2 (Choice = Reverse Buy)
if (rev_buy_hm > buy_hm) and (rev_buy_hm > hold_hm):
    rev_buy = 1
    count_rand_2 += 1

# Condition 3 (Choice = Hold)
if (hold_hm > buy_hm) and (hold_hm > rev_buy_hm):
    hold = 1
    count_rand_3 += 1

check_1 = buy + rev_buy + hold

if check_1 == 0:

    # Condition 4 (Choice = Rand(Buy; Reverse Buy))
    if (buy_hm == rev_buy_hm) and (buy_hm != hold_hm):
        rand_token = random.randint(0, 1)
        if rand_token == 0:
            buy = 1
        else:
            rev_buy = 1
        count_rand_4 += 1

    # Condition 5 (Choice = Rand(Reverse Buy; Hold))
    if (rev_buy_hm == hold_hm) and (rev_buy_hm != buy_hm):
        rand_token = random.randint(0, 1)
        if rand_token == 0:
            rev_buy = 1
        else:
            hold = 1
        count_rand_4 += 1

    # Condition 6 (Choice = Rand(Buy; Hold))
    if (hold_hm == buy_hm) and (hold_hm != rev_buy_hm):
        rand_token = random.randint(0, 1)
        if rand_token == 0:
            hold = 1
        else:
            buy = 1
        count_rand_4 += 1


check_2 = buy + rev_buy + hold

# Condition 7 (Choice = Rand(Buy; Reverse Buy; Hold))
if check_2 == 0:
    rand_token = random.randint(0, 2)
    if rand_token == 0:
        buy = 1
    if rand_token == 1:
        rev_buy = 1
    if rand_token == 2:
        hold = 1
    count_rand_7 += 1
