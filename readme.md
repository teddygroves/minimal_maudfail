# A small example to illustrate when our model fails

# Instructions:

0. Fresh python 3 environment
1. Install python dependencies
```shell
pip install -r requirements.txt
```
2. Install cmdstan 2.27.0
```shell
install_cmdstan --version=2.27.0 --dir=cmdstan
```
3. Install cmdstan 2.27.0-rc1 (requires a few manual steps)
```shell
install_cmdstan --version=2.27.0-rc1 --dir=cmdstan # this step errors
mv cmdstan/cmdstan cmdstan/cmdstan-2.27.0-rc1
cd cmdstan/cmdstan-2.27.0-rc1
make build
cd ../../
```
4. run the script
```shell
python script.py
```

