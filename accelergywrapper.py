"""
AAAAAAAAAAAAAAAAAAAA
We should really put our citations here

Also need to put author names and emails in setup

"""


from typing import Dict
from math import sqrt
import re

AREA_ACCURACY = 1
ENERGY_ACCURACY = 90

WIRE_NAMES = ['wire', 'Wire']
WIRE_ACTIONS = ['energy', 'transfer_random']

DEFAULT_SWITCHING_ACTIVITY_FACTOR = 0.15
SWING_VOLTAGE = 0.5

A_CONSTANT = 1.07

WIRE_CAP_PER_UNIT_LENGTH = { #pf/mm to match Timeloop expectations
    180: .440,
    130: .430,
    100: .403,
    70:  .367,
    50:  .345,
    35:  .315,
    25:  .288,
    18:  .266,
    13:  .247,
}
MIN_TECHNODE = min(WIRE_CAP_PER_UNIT_LENGTH.keys())
MAX_TECHNODE = max(WIRE_CAP_PER_UNIT_LENGTH.keys())

def wire_energy_per_unit_length(
    tech_node: int, delay_penalty: float, voltage: float, switching_activity: float) -> float:
    """ 
    Returns the energy per unit length of a wire.
    tech_node: Technology node of the design in nm
    delay_penalty: Maximum delay overhead in a fraction of the optimal delay. 0 for min delay,
                   1 for doubled delay, 2 for tripled...
    voltage: Wire swing voltage in volts
    switching_activity: Switching activity factor. The probability that a given transmission will
                        flip from 0->1 or 1->0.
    """
    if isinstance(tech_node, str):
        tech_node = int(''.join(re.findall(r'\d', tech_node)))
    assert tech_node >= MIN_TECHNODE, \
        f'Wire energy can not be calculated for {tech_node}nm. Minimum supported: {MIN_TECHNODE}'
    assert tech_node <= MAX_TECHNODE, \
        f'Wire energy can not be calculated for {tech_node}nm. Maximum supported: {MAX_TECHNODE}'
    assert delay_penalty >= 0, f'Wire energy can not be calculated for delay penalty ' \
                               f'{delay_penalty}. Acceptable delay penalty must be non-negative'
    tech_node_lo = max(x for x in WIRE_CAP_PER_UNIT_LENGTH.keys() if x <= tech_node)
    tech_node_hi = min(x for x in WIRE_CAP_PER_UNIT_LENGTH.keys() if x >= tech_node)
    c_lo = WIRE_CAP_PER_UNIT_LENGTH[tech_node_lo]
    c_hi = WIRE_CAP_PER_UNIT_LENGTH[tech_node_hi]
    if tech_node_lo == tech_node_hi:
        cap = c_lo
    else:
        cap = c_lo + (c_hi - c_lo) * (tech_node - tech_node_lo) / (tech_node_hi - tech_node_lo)

    delay_penalty += 1 # Add in minimum delay
        
    a = A_CONSTANT
    asq = A_CONSTANT**2
    dpsq = delay_penalty**2

    dp_a_prod1 = asq - 2 * a * dpsq - dpsq + 1
    # The product of two design knobs on the wire energy and delay penalty
    # This gives values on the mininum energy and delay penalty Pareto curve    
    x_prod = (asq * dpsq - sqrt((-asq * dpsq + dp_a_prod1) ** 2 - 4 * asq) - (dp_a_prod1)) / (2 * a)

    # print(f'Voltage**2: {voltage**2}')
    # print(f'Cap: {cap}')
    # print(f'1+x_prod: {1+x_prod}')
    # print(f'A_CONSTANT: {A_CONSTANT}')

    return switching_activity * voltage**2 * cap * (1+ x_prod * A_CONSTANT)


# ==============================================================================
# Wrapper Class
# ==============================================================================
class WireEstimator:
    def __init__(self):
        self.estimator_name = 'Wire Estimator'

    def primitive_action_supported(self, interface: Dict) -> float:
        """
        :param interface:
        - contains four keys:
        1. class_name : string
        2. attributes: dictionary of name: value
        3. action_name: string
        4. arguments: dictionary of name: value
        :type interface: dict
        :return return the accuracy if supported, return 0 if not
        :rtype: int
        """
        class_name = interface['class_name']
        action_name = interface['action_name']
        #print('Asked me for support for {} {}'.format(class_name, action_name))
        #print(str(class_name).lower() in WIRE_NAMES and str(action_name).lower() in WIRE_ACTIONS)
        if str(class_name).lower() in WIRE_NAMES and str(action_name).lower() in WIRE_ACTIONS:
            return ENERGY_ACCURACY

        return 0  # if not supported, accuracy is 0

    def estimate_energy(self, interface: Dict) -> float:
        """
        :param interface:
        - contains four keys:
        1. class_name : string
        2. attributes: dictionary of name: value
        3. action_name: string
        4. arguments: dictionary of name: value
       :return the estimated energy
       :rtype float
        """
        class_name = interface['class_name']
        attributes = interface['attributes']
        action_name = interface['action_name']

        assert 'technology' in attributes, f'Technology node not specified for wire. Please ' \
                                           f'provide a technology node in nm. Given {attributes}'
        assert 'delay_penalty' in attributes, f'Delay penalty not specified for wire. Please ' \
                                              f'provide a maximum acceptable delay penalty as ' \
                                              f'a fraction of the optimal delay. Given {attributes}'

        if 'voltage' not in attributes:
            print(f'WARNING: Swing voltage not specified for wire. Assuming voltage={SWING_VOLTAGE}V')
        if 'switching_activity' not in attributes:
            print(f'WARNING: Switching activity not specified for wire. ' \
                  f'Assuming switching_activity={DEFAULT_SWITCHING_ACTIVITY_FACTOR}')

        return wire_energy_per_unit_length(
            attributes['technology'], 
            attributes['delay_penalty'], 
            attributes.get('voltage', SWING_VOLTAGE),
            attributes.get('switching_activity', DEFAULT_SWITCHING_ACTIVITY_FACTOR)
        )

    def primitive_area_supported(self, interface: Dict) -> float:
        """
        :param interface:
        - contains two keys:
        1. class_name : string
        2. attributes: dictionary of name: value
        :type interface: dict
        :return return the accuracy if supported, return 0 if not
        :rtype: int
        """
        class_name = interface['class_name']
        attributes = interface['attributes']
        if str(class_name).lower() in WIRE_NAMES:
            return AREA_ACCURACY
        return 0  # if not supported, accuracy is 0

    def estimate_area(self, interface: Dict) -> float:
        """
        :param interface:
        - contains two keys:
        1. class_name : string
        2. attributes: dictionary of name: value
        :type interface: dict
        :return the estimated area
        :rtype: float
        """
        return 0  # if not supported, accuracy is 0
