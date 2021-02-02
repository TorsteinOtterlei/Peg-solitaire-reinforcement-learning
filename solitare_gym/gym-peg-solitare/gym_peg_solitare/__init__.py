
from gym.envs.registration import register

register(
    id='diamond-v0',
    entry_point='gym_peg_solitare.envs:DiamondEnv',
)
register(
    id='triangle-v0',
    entry_point='gym_peg_solitare.envs:TriangleEnv',
)