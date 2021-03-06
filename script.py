"""Configure the variable `DATA_DIRNAME` with the name of a director that lives
in the `data` directory.

The specified directory should contain files called `stan_input_data.json`,
`config.toml` and optionally `inits.json`.

`config.toml` Should have a table `sample_kwargs` with keyword arguments to
`cmdstanpy.CmdStanModel.sample` and a boolean field `use_inits_file` that
specifies whether or not to use `inits.json`.

"""

from cmdstanpy import CmdStanModel, set_cmdstan_path
import os
import toml


# This variable names a directory in `<project_root>/data` to use as input
# data.  Change it (and create an corresponding directory with appropriate
# contents) if you want to test a different input.
DATA_DIRNAME = "methionine_cycle"

MODEL_FILE = "model.stan"
DATA_DIR = os.path.join("data", DATA_DIRNAME)
STAN_INPUT_DATA_FILE = os.path.join(DATA_DIR, "stan_input_data.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.toml")
OUTPUT_DIR = os.path.join("output", DATA_DIRNAME)
CMDSTAN_DIR = "cmdstan"
CMDSTAN_VERSIONS = ["cmdstan-ode-adjoint-v2", "cmdstan-2.27.0", "cmdstan-2.27.0-rc1"]


def main():
    for cmdstan_version in CMDSTAN_VERSIONS:
        print(f"\nTesting cmdstan version {cmdstan_version}...")

        # delete hpp and binary files if they exist
        if os.path.exists("model"):
            os.remove("model")
        if os.path.exists("model.hpp"):
            os.remove("model.hpp")

        # set output directory and create it if it doesn't already exist
        output_dir = os.path.join(OUTPUT_DIR, cmdstan_version)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # use the version of cmdstan at `CMDSTAN_DIR/cmdstsan_version`
        cmdstan_dir = os.path.join(CMDSTAN_DIR, cmdstan_version)
        set_cmdstan_path(cmdstan_dir)

        # compile Stan model
        model = CmdStanModel(stan_file=MODEL_FILE)

        # get arguments to CmdStanModel.sample from the config file
        config = toml.load(CONFIG_FILE)
        sample_kwargs = config["sample_kwargs"]
        if "use_inits_file" in config.keys() and config["use_inits_file"]:
            sample_kwargs["inits"] = os.path.join(DATA_DIR, "inits.json")
        sample_kwargs["output_dir"] = output_dir

        # sample using arguments from config file
        model.sample(data=STAN_INPUT_DATA_FILE, **sample_kwargs)


if __name__ == "__main__":
    main()
