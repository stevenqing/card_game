# card_game
A certain card game named 7王523

# Using guide

1.downloading the card_env.py file to the classic_control/envs/gym/site_packages/python3.7/lib(under anaconda environment)
2.modify the __init__.py/classic_control, adding from gym.envs.classic_control.card_env import CardEnv
3.modyfy the __init__.py/envs, adding 
register(    
    id='CardEnv-v0',
    entry_point='gym.envs.classic_control:CardEnv',
)

