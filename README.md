# Minihack-Treasures-Collector

## Introduction

This project is centered around developing intelligent algorithms for agents to navigate through partially observable environments with optimal reasoning. The primary focus involves implementing an advanced exploration algorithm, based on A*, to enable the agent to effectively address our objectives. The agent's goal is to navigate sensibly within randomly generated rooms. It has to identify specific objects to recognize different room types, locate the target object and reach it. We used NetHack as the foundational framework for this project, offering a rich and complex environment for the development and testing of intelligent exploration algorithms.

## Related works

For generating the random environment in which the agent performs our smart algorithms we used MiniHack and gym libraries.
MiniHack is a software tool tailored for AI experimentation. It provides a simplified version of NetHack Learning Environment (NLE) with reduced complexity. It offers a controlled environment for training and testing AI agents and algorithms.
Gym, by OpenAI, is a toolkit for reinforcement learning that provides a standardized interface for various environments, including MiniHack. In this collaboration, Gym acts as a bridge, allowing AI agents to interact with MiniHack through its standardized interface. By initializing Gym and MiniHack in our Python environment, we developed an AI agent that exploits an optimized searching algorithm to perform our task in a controlled environment. This setup enables efficient experimentation and algorithm refinement for AI tasks within MiniHack.
For creating room shapes and for choosing objects we checked the NetHackWiki. For room exploration we decided to implement a modified version of A* with some optimizations. For this, we exploited the AIMA documentation.pdf) while the heuristics and the optimizations are created by us to let A* perform well in a partially observable environment.

## Task

The main task is to identify the room type the agent is in, among _"Dragon Cave"_, _"Samurai Temple of Doom"_ and _"Abandoned Gold Mines of the Orcs"_, each of which has a three target object, two cursed and one not. The agent's ability to discern room types relies on clue objects. These objects are placed within each room based on the probability of finding them in that specific room type. The collective probabilities of these objects to be inside a room always sum to one. When the agent recognizes the type of room, exceeding a confidence threshold of the probability of being in that room, it consequently understands which target object is safe, reaches and gets it.

## Contributors

Each team member made significant contributions to the entire project, however:

- [Aliprandi Francesco](https://github.com/francealip): object choice, A* implementation and its optimizations
- [De Castelli Fabrizio](https://github.com/FabriDeCastelli): object recognition, code refactoring and assessments
- [Di Riccio Tommaso](https://github.com/tommasoDR): random room generator and map preconditioning
- [Minniti Marco](https://github.com/Marco-Minniti): object recognition and probabilistic reasoning
- [SImonetti Francesco](https://github.com/francescoS01): object choice and room exploration function logic
