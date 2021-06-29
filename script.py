from cmdstanpy import CmdStanModel, set_cmdstan_path
import os
from pathlib import Path

MODEL_FILE = "model.stan"
DATA_FILE = os.path.join("data", "linear.json")
OUTPUT_DIR = os.path.join("output", "linear")
SAMPLE_KWARGS = {
    "chains": 1,
    "iter_warmup": 10,
    "iter_sampling": 10,
    "metric": "dense"
}
CMDSTAN_DIR = "cmdstan"
CMDSTAN_VERSIONS = ["cmdstan-2.27.0", "cmdstan-2.27.0-rc1"]
CMDSTAN_DIRS = [os.path.join(CMDSTAN_DIR, d) for d in CMDSTAN_VERSIONS]

def main():
    for cmdstan_version in CMDSTAN_VERSIONS:
        print(f"\nTesting cmdstan version {cmdstan_version}...")
        output_dir = os.path.join(OUTPUT_DIR, cmdstan_version)
        cmdstan_dir = os.path.join(CMDSTAN_DIR, cmdstan_version)
        set_cmdstan_path(cmdstan_dir)
        sample_kwargs = SAMPLE_KWARGS.copy()
        sample_kwargs["output_dir"] = output_dir
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        model = CmdStanModel(stan_file=MODEL_FILE, compile=False)
        model.compile(force=True)
        fit = model.sample(data=DATA_FILE, **sample_kwargs)


if __name__ == "__main__":
    main()
