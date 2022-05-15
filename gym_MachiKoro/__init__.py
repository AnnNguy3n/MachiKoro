from gym.envs.registration import register

register(
    id = 'gym_MachiKoro-v0',    
    entry_point = 'gym_MachiKoro.envs:MachiKoro_Env',
)