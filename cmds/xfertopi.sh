set -ue # or set -o nounset
: "$PIHOME"
deactivate || true

BACKUP_FOLDER="code_`date +%s`"
SOURCE=/home/alexb/Docs/pokemon_card_game/code # $PIHOME/code
DEST=pi@192.168.6.62:/home/pi/$BACKUP_FOLDER
rsync --no-i-r --info=progress2 -a --exclude=".pokemonpyenv" $SOURCE $DEST
