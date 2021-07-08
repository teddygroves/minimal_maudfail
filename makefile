.phony: clean-results clean-cmdstan stan-environment python-requirements

QUOTE_LINES = sed "s/^/'/;s/$$/'/"  # pipe this to make sure filenames are quoted
OUTPUT_CSVS = $(shell find output -type f -name "*.csv" | $(QUOTE_LINES))
OUTPUT_TXTS = $(shell find output -type f -name "*.txt" | $(QUOTE_LINES))
CMDSTAN_2270 = cmdstan/cmdstan-2.27.0
CMDSTAN_2270_rc1 = cmdstan/cmdstan-2.27.0-rc1
CMDSTAN_ODE_ADJOINT_V2 = cmdstan/cmdstan-ode-adjoint-v2
REQUIREMENTS_FILE = requirements.txt
MODEL_BINARY_FILE = model
MODEL_HPP_FILE = model.hpp

ifeq ($(OS),Windows_NT)
	MAKE_PROGRAM = mingw32-make
else
	MAKE_PROGRAM = make
endif

stan-environment: python-requirements $(CMDSTAN_ODE_ADJOINT_V2) $(CMDSTAN_2270) $(CMDSTAN_2270_rc1)

python-requirements: $(REQUIREMENTS_FILE)
	pip install -r requirements.txt

$(CMDSTAN_2270): python-requirements
	install_cmdstan --version=2.27.0 --dir=cmdstan

# "-" at start of first line is for continuing after error
# lines 2 and 3 correct the bad directory name and build cmdstan manually
$(CMDSTAN_2270_rc1): python-requirements
	-install_cmdstan --version=2.27.0-rc1 --dir=cmdstan 
	-mv cmdstan/cmdstan cmdstan/cmdstan-2.27.0-rc1
	cd cmdstan/cmdstan-2.27.0-rc1 && $(MAKE_PROGRAM) build

$(CMDSTAN_ODE_ADJOINT_V2): python-requirements
	cd cmdstan && wget -c https://github.com/rok-cesnovar/cmdstan/releases/download/adjoint_ODE_v2/cmdstan-ode-adjoint-v2.tar.gz -O - | tar -xz
	cd $(CMDSTAN_ODE_ADJOINT_V2) && $(MAKE_PROGRAM) build

clean-stan:
	$(RM) $(MODEL_BINARY_FILE) $(MODEL_HPP_FILE)

clean-results:
	$(RM) $(OUTPUT_CSVS)
	$(RM) $(OUTPUT_TXTS)

clean-cmdstan:
	$(RM) -rf $(CMDSTAN_2270)
	$(RM) -rf $(CMDSTAN_2270_rc1)
