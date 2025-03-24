set -ue # or set -o nounset
: "$PIHOME"
deactivate || true

BACKUP_FOLDER="pibackup_`date +%s`"
SOURCE=pi@pokepi.local:/home/pi/*
DEST=$HOME/$BACKUP_FOLDER
rsync --no-i-r --info=progress2 -a --exclude=".pokemonpyenv" $SOURCE $DEST
