from gym.envs.registration import register

register(
    id='lb-v0',
    entry_point='gym_lb.envs:LbEnv',
)