import numpy as np

def gartley(current_pat, err=float):
    XA = current_pat[1] - current_pat[0]
    AB = current_pat[2] - current_pat[1]
    BC = current_pat[3] - current_pat[2]
    CD = current_pat[4] - current_pat[3]

    AB_range = np.array([0.618 - err, 0.618 + err]) * abs(XA)
    BC_range = np.array([0.382 - err, 0.886 + err]) * abs(AB)
    CD_range = np.array([1.27 - err, 1.618 + err]) * abs(BC)

    if XA > 0 > AB and BC > 0 > CD:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            return 1, 'Bullish Gartley'

    elif XA < 0 < AB and BC < 0 < CD:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            return -1, 'Brearish Gartley'


def butterfly(current_pat, err=float):
    XA = current_pat[1] - current_pat[0]
    AB = current_pat[2] - current_pat[1]
    BC = current_pat[3] - current_pat[2]
    CD = current_pat[4] - current_pat[3]

    AB_range = np.array([0.786 - err, 0.786 + err]) * abs(XA)
    BC_range = np.array([0.382 - err, 0.886 + err]) * abs(AB)
    CD_range = np.array([1.618 - err, 2.618 + err]) * abs(BC)

    if XA > 0 > AB and BC > 0 > CD:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            return 1, 'Bullish Butterfly'

    elif XA < 0 < AB and BC < 0 < CD:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            return -1, 'Brearish Butterfly'


def bat(current_pat, err=float):
    XA = current_pat[1] - current_pat[0]
    AB = current_pat[2] - current_pat[1]
    BC = current_pat[3] - current_pat[2]
    CD = current_pat[4] - current_pat[3]

    AB_range = np.array([0.382 - err, 0.5 + err]) * abs(XA)
    BC_range = np.array([0.382 - err, 0.886 + err]) * abs(AB)
    CD_range = np.array([1.618 - err, 2.618 + err]) * abs(BC)

    if XA > 0 > AB and BC > 0 > CD:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            return 1, 'Bullish Bat'

    elif XA < 0 < AB and BC < 0 < CD:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            return -1, 'Brearish Bat'


def crab(current_pat, err=float):
    XA = current_pat[1] - current_pat[0]
    AB = current_pat[2] - current_pat[1]
    BC = current_pat[3] - current_pat[2]
    CD = current_pat[4] - current_pat[3]

    AB_range = np.array([0.382 - err, 0.618 + err]) * abs(XA)
    BC_range = np.array([0.382 - err, 0.886 + err]) * abs(AB)
    CD_range = np.array([2.24 - err, 3.618 + err]) * abs(BC)

    if XA > 0 > AB and BC > 0 > CD:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            return 1, 'Bullish Crab'

    elif XA < 0 < AB and BC < 0 < CD:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            return -1, 'Brearish Crab'
