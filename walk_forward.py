def walk_forward(cprice, lprice, hprice, atr, sign, balance, risk_threshold, multiplier, fee):
    # return 1, 1, 0
    if sign == 1:
        initial_stop_loss = cprice[0] - (multiplier * atr[0])
        stop_loss = initial_stop_loss

        initial_risk = (cprice[0] - initial_stop_loss) / cprice[0]
        position_size = (risk_threshold / initial_risk) * balance * (1 - 2 * fee)

        for i in range(1, len(cprice)):

            move = cprice[i] - cprice[i-1]

            if lprice[i] < stop_loss:
                position_result_percent = (stop_loss / cprice[0]) - 1
                trade_result = (position_size * position_result_percent)

                paid_fee = fee * ((2 * position_size) + trade_result)
                return trade_result, i, paid_fee

            elif move > 0 and (cprice[i] - (multiplier * atr[i])) > stop_loss:
                stop_loss = cprice[i] - (multiplier * atr[i])

        # If stop loss never get hit, return final values
        position_result_percent = (cprice[-1] / cprice[0]) - 1
        trade_result = (position_size * position_result_percent)
        paid_fee = fee * ((2 * position_size) + trade_result)

        return trade_result, len(cprice)-1, paid_fee



    elif sign == -1:
        initial_stop_loss = cprice[0] + (multiplier * atr[0])
        stop_loss = initial_stop_loss

        initial_risk = (initial_stop_loss - cprice[0]) / cprice[0]
        position_size = (risk_threshold / initial_risk) * balance * (1 - 2 * fee)

        for i in range(1, len(cprice)):

            move = cprice[i] - cprice[i - 1]

            if hprice[i] > stop_loss:
                position_result_percent = 1 - (stop_loss / cprice[0])
                trade_result = position_size * position_result_percent

                paid_fee = fee * ((2 * position_size) + trade_result)
                return trade_result, i, paid_fee

            elif move < 0 and (cprice[i] + (multiplier * atr[i])) < stop_loss:
                stop_loss = cprice[i] + (multiplier * atr[i])

        # If the stop loss is never hit, return final values
        position_result_percent = 1 - (cprice[-1] / cprice[0])
        trade_result = position_size * position_result_percent
        paid_fee = fee * ((2 * position_size) + trade_result)

        return trade_result, len(cprice)-1, paid_fee
