import random
import statsmodels.api as sm

# input alpha, penalty, + 2 files ("db.txt, ticket_prices.txt")

output_dir = ['Output/0.1/Frequentist/', 'Output/0.3/Frequentist/', 'Output/0.5/Frequentist/', 'Output/0.7/Frequentist/', 'Output/0.9/Frequentist/']

output_half_dir = ['Output/0.1_H/Frequentist/', 'Output/0.3_H/Frequentist/', 'Output/0.5_H/Frequentist/', 'Output/0.7_H/Frequentist/', 'Output/0.9_H/Frequentist/']


def frequentist_player(alpha, penalty, file_1, file_2, var, p, full):
    ###############################################
    # PARAMETERS SETTING FOR THE FREQUENTIST PLAYER#
    ###############################################

    pen = penalty
    # alpha = 0.05
    # This is the significance level we set at the beginning of our games

    L = 0
    U = 1
    # initial confidence interval bounds

    # penalty = 1
    # A cost between 0 and 1 USD that penalizes the player in case of hold.

    ###############################################
    ###############################################
    ###############################################

    f = open(file_1, 'r')
    raw_list = f.readlines()

    raw_list = list(map(lambda x: x.strip(), raw_list))

    setting_info = raw_list[0].split('$')
    setting_info = list(filter(None, setting_info))
    setting_info = list(map(int, setting_info))
    raw_list = list(map(int, raw_list[1:]))
    game_list = [raw_list[i:i + setting_info[2]] for i in range(0, len(raw_list), setting_info[2])]

    f.close()

    f = open(file_2, 'r')
    raw_price_list = f.readlines()

    raw_price_list = list(map(lambda x: x.strip(), raw_price_list))
    price_list = list(map(float, raw_price_list))

    f.close()

    m = setting_info[1]
    # m is the number of played games

    # print('We have set ', m, ' games for this simulation')
    # print('')

    coin_bias = setting_info[0] / 1000
    # << coin_bias >> is a real number between 0 and 1.
    # An approximation to 3 decimal rational numbers is performed.
    # If << coin_bias = 0 >>, the game admits only tails as a result.
    # If << coin_bias = 0.5 >>, the toss is fair.
    # If << coin_bias = 1 >>, the game admits only heads as a result.

    # print('For each game, the coin bias is set to', coin_bias)
    # print('')

    num_coin_tosses = setting_info[2]
    # << num_coin_tosses >> is a natural number that set the number of coin tosses
    # for each m-game.

    # print('For each game, ', num_coin_tosses, ' draws are expected to occour.')
    # print('')

    # print('The penalty price is set to USD ', penalty)
    # print('')

    profit = 0
    # This is the initial profit

    simulation_profit = list()
    # This is the list where we store all profits obtained in this simulation

    coin_bias_mod = setting_info[0]

    # print('For each game, the significance level -- alpha -- is set to', alpha)
    # print('')

    # print('At the beginning of game n. 1, the confidence interval is set to [' + str(L) + '; ' + str(U) + ']')
    # print('')

    H = 0
    T = 0
    N = 0
    count_rand_1 = 0
    count_rand_2 = 0
    count_rand_3 = 0
    count_rand_4 = 0
    count_rand_5 = 0
    count_rand_6 = 0
    count_rand_7 = 0

    for j in range(0, m):
        if penalty == 2:
            penalty = 0.1 * random.random()
        h = 0
        t = 0
        in_game_profit = 0
        buy = 0
        rev_buy = 0
        hold = 0
        check_1 = 0
        check_2 = 0
        betting_check = 0
        coin_tosses_list = game_list[j]
        # print('This is game n.', j + 1, ' and these are its ', num_coin_tosses, 'draws:')
        string_coin_tosses = '['
        for k in range(0, len(coin_tosses_list)):
            if k == len(coin_tosses_list) - 2:
                string_coin_tosses = string_coin_tosses + str(coin_tosses_list[k]) + ']'
            if k == len(coin_tosses_list) - 1:
                string_coin_tosses = string_coin_tosses + '(' + str(coin_tosses_list[k]) + ')'
                betting_coin_toss = coin_tosses_list[k]
            if k != len(coin_tosses_list) - 2 and k != len(coin_tosses_list) - 1:
                string_coin_tosses = string_coin_tosses + str(coin_tosses_list[k]) + ' '
        # print(string_coin_tosses)
        # print('')
        num_heads = sum(coin_tosses_list) - betting_coin_toss
        num_tails = num_coin_tosses - num_heads - 1
        h = num_heads
        # local absolute head frequency
        t = num_tails
        # local absolute tail frequency
        # print('The head frequency for this game is ', h)
        # print('')
        # print('The tail frequency for this game is ', t)
        if j != 0:
            H = h + H
        else:
            H = h
        # global absolute head frequency
        if j != 0:
            T = t + T
        else:
            T = t
        # global absolute head frequency
        # print('')
        # print('The cumulative head frequency for this game is ', H)
        # print('')
        # print('The cumulative tail frequency for this game is ', T)
        ticket_price = price_list[j]
        # print('')
        # print('The ticket price for this game is USD ', round(ticket_price, 3))
        # print('')

        N = H + T
        conf_int = sm.stats.proportion_confint(H, N, alpha, method='beta')
        L = conf_int[0]
        U = conf_int[1]
        # Updating confidence interval

        # print('The updated confidence interval is [' + str(round(L, 3)) + '; ' + str(round(U, 3)) + ']')
        # print('')

        min_ut_straight_bet = (L * (1 - ticket_price)) - (ticket_price * (1 - L))
        min_ut_reverse_bet = (U * (-(1 - ticket_price))) + (ticket_price * (1 - U))
        min_ut_hold = -penalty
        # Computation of minimum utilities
        max_ut_straight_bet = (U * (1 - ticket_price)) - (ticket_price * (1 - U))
        max_ut_reverse_bet = (L * (-(1 - ticket_price))) + (ticket_price * (1 - L))
        max_ut_hold = -penalty
        # Computation of maximum utilities

        # Condition 1
        if (min_ut_straight_bet > max_ut_reverse_bet) and (min_ut_straight_bet > max_ut_hold):
            buy = 1
            count_rand_1 += 1

        # Condition 2
        if (min_ut_reverse_bet > max_ut_straight_bet) and (min_ut_reverse_bet > max_ut_hold):
            rev_buy = 1
            count_rand_2 += 1

        # Condition 3
        if (min_ut_hold > max_ut_straight_bet) and (min_ut_hold > max_ut_reverse_bet):
            hold = 1
            count_rand_3 += 1

        check_1 = buy + rev_buy + hold

        if check_1 == 0:

            # Condition 4
            if (min_ut_straight_bet > max_ut_reverse_bet) and (min_ut_hold > max_ut_reverse_bet):
                rand_token = random.randint(0, 1)
                if rand_token == 0:
                    buy = 1
                else:
                    hold = 1
                count_rand_4 += 1

            # Condition 5
            if (min_ut_straight_bet > max_ut_hold) and (min_ut_reverse_bet > max_ut_hold):
                rand_token = random.randint(0, 1)
                if rand_token == 0:
                    buy = 1
                else:
                    rev_buy = 1
                count_rand_5 += 1

            # Condition 6
            if (min_ut_reverse_bet > max_ut_straight_bet) and (min_ut_hold > max_ut_straight_bet):
                rand_token = random.randint(0, 1)
                if rand_token == 0:
                    rev_buy = 1
                else:
                    hold = 1
                count_rand_6 += 1

        check_2 = buy + rev_buy + hold

        # Condition 7
        if check_2 == 0:
            rand_token = random.randint(0, 2)
            if rand_token == 0:
                buy = 1
            if rand_token == 1:
                rev_buy = 1
            if rand_token == 2:
                hold = 1
            count_rand_7 += 1

        betting_check = buy + rev_buy

        if betting_coin_toss == 1 and betting_check != 0 and hold == 0:
            if buy == 1 and rev_buy == 0:
                in_game_profit = (1 - ticket_price)
                profit = profit + (1 - ticket_price)
            if buy == 0 and rev_buy == 1:
                in_game_profit = -(1 - ticket_price)
                profit = profit - (1 - ticket_price)
        else:
            if buy == 1 and rev_buy == 0:
                in_game_profit = -ticket_price
                profit = profit - ticket_price
            if buy == 0 and rev_buy == 1:
                in_game_profit = ticket_price
                profit = profit + ticket_price
        if betting_check == 0 and hold != 0:
            in_game_profit = -penalty
            profit = profit - penalty

        if betting_coin_toss == 1:
            H = H + 1
        else:
            T = T + 1

        # if buy == 1:
        # print('The player has decided to BUY A TICKET')
        # if rev_buy == 1:
        # print('The player has decided to BUY A REVERSE TICKET')
        # if hold == 1:
        # print('The player has decided to HOLD')
        # print('')

        # print('The profit for this game is USD ', round(in_game_profit, 3))
        # print('')
        # print('The cumulated profit is USD ', round(profit, 3))
        # print('')
        # print('*****')
        # print('')
        simulation_profit.append(profit)

    if pen == 2:
        penalty = pen
    if full:
        filename = output_dir[p] + 'Frequentist_results_' + 'full' + '_coin_bias_' + output_dir[p][
                                                                                    7:10] + '_alpha=' + str(
            alpha) + '_penalty=' + str(penalty) + '_' + str(var) + '.txt'
    else:
        filename = output_half_dir[p] + 'Frequentist_results_' + 'half' + '_coin_bias_' + output_half_dir[p][
                                                                                    7:12] + '_alpha=' + str(
            alpha) + '_penalty=' + str(penalty) + '_' + str(var) + '.txt'

    with open(filename, 'w') as f:
        for item in simulation_profit:
            f.write("%s\n" % item)

    # print('Simulated profits have been correctly saved into ' + filename + ' file.')
    # print('')

    f.close()


    count_rand=list()
    count_rand=[count_rand_1, count_rand_2, count_rand_3, count_rand_4, count_rand_5, count_rand_6, count_rand_7]

    filename_1='Frequentist_statistics_alpha='+str(alpha)+'_penalty='+str(penalty)+'.txt'

    if full:
        filename_1 = output_dir[p] + 'Frequentist_statistics_' + 'full' + '_coin_bias_' + output_dir[p][
                                                                                    7:10] + '_alpha=' + str(
            alpha) + '_penalty=' + str(penalty) + '_' + str(var) + '.txt'
    else:
        filename_1 = output_half_dir[p] + 'Frequentist_statistics_' + 'half' + '_coin_bias_' + output_half_dir[p][
                                                                                    7:12] + '_alpha=' + str(
            alpha) + '_penalty=' + str(penalty) + '_' + str(var) + '.txt'

    with open(filename_1, 'w') as f:
        for item in count_rand:
            f.write("%s\n" % item)

    # print('Statistics have been correctly saved into '+filename_1+' file.')
    # print('')

    f.close()

