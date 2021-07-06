# Put input data folders here!

This folder is for input data directories.

A data directory should contain files called `stan_input_data.json`,
`config.toml` and optionally `inits.json`.

`config.toml` Should have a table `sample_kwargs` with keyword arguments to
`cmdstanpy.CmdStanModel.sample` and a boolean field `use_inits_file` that
specifies whether or not to use `inits.json`.
