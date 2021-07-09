# A small example to illustrate when our model fails

We have been trying to fit Bayesian models of metabolic networks with Stan -
check out our progress [here](https://github.com/biosustain/Maud). Our models'
speed is limited by the need to solve ODEs with large numbers of parameters
compared to the number of state variables, so we are hopeful of being able to
achieve a speedup using Stan's new adjoint ODE solver.

However, starting with cmdstan version 2.27.0-rc1 we began to see some errors
that were not occurring before, and the sampler started to behave
strangely. This repository provides an example that reproduces this error.

# Requirements
- wget
- tar
- make
- C++ toolchain
- Python 3.7+

# Instructions:

0. Fresh python 3 environment
```
python -m venv venv_maudfail
source venv_maudfail/bin/activate
```
1. Install cmdstanpy, cmdstanv versions cmdstan-ode-adjoint-v2, cmdstan-2.27.0-rc1 and cmdstan-2.27.0 (the cmdstans go in the directory `cmdstan`)
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

The python file `script.py` is quite lightweight - it just sets the version of
cmdstan that cmdstanpy will use, deletes any model files, compiles a new model
using cmdstanpy and samples with it using the input data json file, inits json
file and sampler configuration toml file from the folder
`data/methionine_cycle`.

To change the sampler configuration, edit the table `sample_kwargs` in the file
`data/methionine_cycle/config.toml`.

To change the ode tolerances, edit the file
`data/methionine_cycle/stan_input_data.json`.

To change the initial parameter values, edit the file
`data/methionine_cycle/inits.json`.

To remove all cmdstan folders, run `make clean-cmdstan`.

to remove all Stan output files, run `make clean-results`.
