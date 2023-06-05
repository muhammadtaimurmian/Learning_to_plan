import socket
import struct
import pickle
import numpy as np
import os
import gym
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.monitor import Monitor
import argparse

class Connection:
    def __init__(self, s):
        self._socket = s
        self._buffer = bytearray()

    def receive_object(self):
        while len(self._buffer) < 4 or len(self._buffer) < struct.unpack("<L", self._buffer[:4])[0] + 4:
            new_bytes = self._socket.recv(16)
            if len(new_bytes) == 0:
                return None
            self._buffer += new_bytes
        length = struct.unpack("<L", self._buffer[:4])[0]
        header, body = self._buffer[:4], self._buffer[4:length + 4]
        obj = pickle.loads(body)
        self._buffer = self._buffer[length + 4:]
        return obj

    def send_object(self, d):
        body = pickle.dumps(d, protocol=2)
        header = struct.pack("<L", len(body))
        msg = header + body
        self._socket.send(msg)


class Env(gym.Env):
    def __init__(self, addr):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(addr)
        s.listen(1)
        clientsocket, address = s.accept()

        self._socket = clientsocket
        self._conn = Connection(clientsocket)

        self.action_space = gym.spaces.Discrete(2)  # when you define the new action, change the action_space.
        self.observation_space = gym.spaces.Box(low=0., high=1., shape=(
        10,))  # when you define a new observation, you should change the number of low,high and shape.

    def reset(self):
        self._conn.send_object("reset")
        msg = self._conn.receive_object()
        self.action_space = eval(msg["info"]["action_space"])
        self.observation_space = eval(msg["info"]["observation_space"])
        return msg["observation"]


    def step(self, action):
        self._conn.send_object(action.tolist())
        msg = self._conn.receive_object()
        obs = msg["observation"]
        rwd = msg["reward"]
        done = msg["done"]
        info = msg["info"]
        return obs, rwd, done, info


    def close(self):
        self._conn.send_object("close")
        self._socket.close()


addr = ("127.0.0.1", 50710)
env = Monitor(Env(addr))
obs = env.reset()


num_experiments = 1  # give a number for experiments

for i in range(num_experiments):
    seed = np.random.randint(0, 1000)
    log_dir = 'DQN_seed' + '_seed' + str(seed) + '__' + str(
        i)  # you can find the file of experiments in the C:\users\userName folder
    os.makedirs(log_dir)
    checkpoint_callback = CheckpointCallback(save_freq=4500, save_path='./' + str(log_dir),
                                             name_prefix='model')
    model = DQN('MlpPolicy', env, learning_rate=3e-3, gamma=0.99, learning_starts=10000, train_freq=1,
                target_update_interval=100, seed=seed, batch_size=128, verbose=1, exploration_fraction=0.65,
                tensorboard_log="./" + str(log_dir))
    # hyperparameters can be adjusted in different projects
    model.learn(total_timesteps=20000, log_interval=1, callback=checkpoint_callback)
    env.reset()


parser = argparse.ArgumentParser()
parser.add_argument('--load-path', help='specify path to model that should be loaded')
args = parser.parse_args()
args.load_path = 'DQN_seed_seed581__0/model_18000_steps.zip'

model = DQN.load(args.load_path, env=env)

cum_rwd = 0
obs = env.reset()
for i in range(500):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    print(i, action, reward, done, info)
    if done:
        obs = env.reset()
        print("Return = ", cum_rwd)
        cum_rwd = 0
env.close()