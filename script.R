"""Configure the variable `DATA_DIRNAME` with the name of a director that lives
in the `data` directory.

The specified directory should contain files called `stan_input_data.json`,
`config.toml` and optionally `inits.json`.

`config.toml` Should have a table `sample_kwargs` with keyword arguments to
`cmdstanpy.CmdStanModel.sample` and a boolean field `use_inits_file` that
specifies whether or not to use `inits.json`.
"""
library("cmdstanr")
library("configr")

modelName <- "methionine_cycle" # Change model here ["linear", "methionine_cycle", "G6PtoPEP"]
setwd(dirname(getActiveDocumentContext()$path)) 
stanModelFile <- "model.stan"
dataDir <- file.path("data", modelName)
stanInputDataFile <- file.path(dataDir, "stan_input_data.json")
configFile <- file.path(dataDir, "config.toml")
outputDir <- file.path("output", modelName)
if (!(dir.exists(outputDir))){
  dir.create(outputDir)
}
cmdstanDirBase <- "cmdstan"
cmdstanVersions <- c("cmdstan-ode-adjoint-v2", "cmdstan-2.27.0", "cmdstan-2.27.0-rc1")
for (i in 1:length(cmdstanVersions)){
  if (file.exists("model")){
    file.remove("model")
  }
  if (file.exists("model.hpp")){
    file.remove("model.hpp")
  }
  cmdstanVersion <- cmdstanVersions[i]
  cmdstanDir <- file.path(cmdstanDirBase, cmdstanVersion)
  print(sprintf('Testing cmdstan version %s', cmdstanVersion))
  outputDirCmdstan <- file.path(outputDir, cmdstanVersion)
  set_cmdstan_path(cmdstanDir)
  config <- read.config(configFile)
  sampleKwargs <- config$sample_kwargs
  if (!dir.exists(outputDirCmdstan)){
    dir.create(outputDirCmdstan)
  }
  sampleKwargs$inits <- 0
  if (with(config, exists("use_inits_file"))){
    sampleKwargs$inits <- file.path(dataDir, "inits.json")
  }
  sampleKwargs$output_dir <- outputDirCmdstan
  if (!(dir.exists(outputDirCmdstan))){
    dir.create(outputDirCmdstan)
  }
  mod <- cmdstan_model(stanModelFile, include_paths = ".")
  mod$sample(data=stanInputDataFile, 
             chains=sampleKwargs$chains,
             iter_sampling=sampleKwargs$iter_sampling,
             iter_warmup=sampleKwargs$iter_warmup,
             refresh=sampleKwargs$refresh,
             save_warmup=sampleKwargs$save_warmup,
             output_dir=sampleKwargs$output_dir,
             step_size=sampleKwargs$step_size,
             metric=sampleKwargs$metric,
             max_treedepth=sampleKwargs$max_treedepth,
             init=sampleKwargs$inits)
}

