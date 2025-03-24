set -ue # or set -o nounset
: "$PIHOME"
deactivate || true

sudo apt install -y python3-dev

# clean poke-env and posho
cd $PIHOME/code/
if [ ! -d poke-env ]; then
    git clone https://github.com/hsahovic/poke-env
fi
cd $PIHOME/code/poke-env
git reset --hard
git clean -xdf
git pull
# chmod +x reinstall.sh
# ./reinstall.sh

# create venv
cd $PIHOME/code/
rm -rf $PIHOME/code/.pokemonpyenv
python3 -m venv .pokemonpyenv
. $PIHOME/code/.pokemonpyenv/bin/activate
cp $PIHOME/code/assets/req* $PIHOME/code/poke-env
pip install -r $PIHOME/code/poke-env/requirements-dev.txt
pip install -r $PIHOME/code/poke-env/requirements.txt
pip install adafruit-circuitpython-pn532
pip install grpcio grpcio-tools

# cd $PIHOME/code/
# if [ ! -d pokemon-showdown ]; then
#     git clone https://github.com/smogon/pokemon-showdown
# fi
# cd $PIHOME/code/pokemon-showdown
# git reset --hard
# git clean -xdf
# git pull
# npm update

echo . $PIHOME/code/.pokemonpyenv/bin/activate
