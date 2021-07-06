# A small example to illustrate when our model fails

We have been trying to fit Bayesian models of metabolic networks with Stan -
check out our progress [here](https://github.com/biosustain/Maud). Our models'
speed is limited by the need to solve ODEs with large numbers of parameters
compared to the number of state variables, so we are hopeful of being able to
achieve a speedup using Stan's new adjoint ODE solver.

However, starting with cmdstan version 2.27.0 we began to see some errors that
were not thrown in version 2.27.0-rc1. This repository provides an example that
reproduces this error.

# Instructions:

0. Fresh python 3 environment
```
python -m venv venv_maudfail
source venv_maudfail/bin/activate
```
1. Install cmdstanpy, cmdstan 2.27.0 and cmdstan2.27.0-rc1 (the last two go to the directory `cmdstan`)
```shell
make stan-environment
```
2. run the script
```shell
python script.py
```
3. Check out the results
```shell
ls output/linear/*
```
