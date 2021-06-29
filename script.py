from cmdstanpy import CmdStanModel, _DOT_CMDSTANPY
import os
from pathlib import Path

MODEL_FILE = "model.stan"
DATA_FILE = os.path.join("data", "linear.json")
OUTPUT_DIR = os.path.join("output", "linear")
SAMPLE_KWARGS = {
    "chains": 1,
    "iter_warmup": 10,
    "iter_sampling": 10,
}
DOT_CMDSTANPY_DIR = os.path.join(Path.home(), ".cmdstanpy")
CMDSTAN_VERSIONS = [
    os.path.join(DOT_CMDSTANPY_DIR, d)
    for d in ["cmdstan-2.27.0", "cmdstan-2.27.0-rc1"]
]

def main():
    for cmdstan_version in CMDSTAN_VERSIONS:
        print(f"\nTesting cmdstan version {cmdstan_version}...")
        sample_kwargs = SAMPLE_KWARGS.copy()
        sample_kwargs["output_dir"] = os.path.join(OUTPUT_DIR, cmdstan_version)
        os.environ["CMDSTAN"] = cmdstan_version
        model = CmdStanModel(stan_file=MODEL_FILE, compile=False)
        model.compile(force=True)
        fit = model.sample(data=DATA_FILE, **sample_kwargs)


if __name__ == "__main__":
    main()
