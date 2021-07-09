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

DATA_DIRNAME = "methionine_cycle"

MODEL_FILE = "model.stan"
DATA_DIR = os.path.join("data", DATA_DIRNAME)
STAN_INPUT_DATA_FILE = os.path.join(DATA_DIR, "stan_input_data.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.toml")
OUTPUT_DIR = os.path.join("output", DATA_DIRNAME)
CMDSTAN_DIR = "cmdstan"
CMDSTAN_VERSIONS = ["cmdstan-ode-adjoint-v2", "cmdstan-2.27.0", "cmdstan-2.27.0-rc1"]
CMDSTAN_DIRS = [os.path.join(CMDSTAN_DIR, d) for d in CMDSTAN_VERSIONS]

def main():
    for cmdstan_version in CMDSTAN_VERSIONS:
        if os.path.exists("model"):
            os.remove("model")
        if os.path.exists("model.hpp"):
            os.remove("model.hpp")
        print(f"\nTesting cmdstan version {cmdstan_version}...")
        output_dir = os.path.join(OUTPUT_DIR, cmdstan_version)
        cmdstan_dir = os.path.join(CMDSTAN_DIR, cmdstan_version)
        set_cmdstan_path(cmdstan_dir)
        config = toml.load(CONFIG_FILE)
        sample_kwargs = config["sample_kwargs"]
        if "use_inits_file" in config.keys() and config["use_inits_file"]:
            sample_kwargs["inits"] = os.path.join(DATA_DIR, "inits.json")
        sample_kwargs["output_dir"] = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        model = CmdStanModel(stan_file=MODEL_FILE)
        model.sample(data=STAN_INPUT_DATA_FILE, **sample_kwargs)


if __name__ == "__main__":
    main()
