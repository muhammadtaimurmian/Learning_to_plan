# Learning_to_plan
This project is the result of a joint effort between myself and Jeremiah Grace Oonyu, conducted at the Institute for Advanced Architecture of Catalonia (IAAC). It was part of the innovative course "AI in the Built Environment", which was expertly led by Angelos Chronis and Serjoscha Duering.

This code is based on a project by Boris Belousov. We found his work helpful and used it as a guide. You can check out Belousov's project through the provided link.

Youtube : https://www.youtube.com/watch?v=KGCvldN5Fpc
Paper : http://papers.cumincad.org/data/works/att/ecaade2021_247.pdf
Github : https://github.com/b4be1/rl-for-sequential-assembly

The grasshopper file is used to construct the environment. This is where the observation space, reward funciton, reset condition and rules of the project are defined. The user can create there own custom environment and make changes to any part of the code as deemed necessary except for the two components demonstrated in the illustration below. Instead use the ouptut of the first component "itteration" and "action" as necessary. Once you have defined your experiment, plug the "observation", "reward", "done" and "action" to the final component. The two components are used to communicate with an external IDE which is used for the learning process.

<img width="541" alt="image" src="https://github.com/muhammadtaimurmian/Learning_to_plan/assets/119614192/85601c65-7fba-4fa2-b125-9c0f77b3a804">

The only change that might be necessary to the above shown components would be in the second component in case you need to change the action_space or the observation_space. This can be done by double clicking the second python component and making the necessary changes.

<img width="838" alt="image" src="https://github.com/muhammadtaimurmian/Learning_to_plan/assets/119614192/7cae84d3-67c4-4714-b926-3db7c58cb759">

