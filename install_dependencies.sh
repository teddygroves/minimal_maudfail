pip install -r requirements.txt

install_cmdstan --version=2.27.0 --dir=cmdstan

install_cmdstan --version=2.27.0-rc1 --dir=cmdstan # build step errors so do manually...

mv cmdstan/cmdstan cmdstan/cmdstan-2.27.0-rc1
cd cmdstan/cmdstan-2.27.0-rc1
make build

cd ../../
