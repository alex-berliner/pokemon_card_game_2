# Pokemon Cards Online

## Intro
This project provides a set of tools for interfacing with Pokemon Showdown to play online battles with real Pokemon cards!

[demo.webm](https://github.com/user-attachments/assets/be0a4c21-8879-446a-8b87-abc9e598ae17)

It can connect to real Pokemon Showdown servers to play against online players, or two clients can connect together to play head-to-head locally.

## Software setup
Only [Raspberry Pi OS](https://www.raspberrypi.com/software/) is supported.

Raspberry Pi OS dependencies:

`sudo apt install -y npm libopenblas-dev`

Get the repository

`git clone https://github.com/alex-berliner/pokemon_card_game --recursive`

Set var for repository's base directory

`export PCO_BASE=<Your repo location>`

Run `./scripts/setup.sh`. This creates and updates your python environment and generates the required protobufs.

## Hardware requirements
- Raspberry Pi 3 or greater
  - Pi 5 required if running the Pokemon Showdown server locally
- [PN532 dev board](https://www.elechouse.com/product/pn532-nfc-rfid-module-v4/)
- [MIFARE Classic 1K Tags](https://www.sparkfun.com/rfid-tag-adhesive-mifare-classicr-1k-13-56-mhz.html)

## Setup

### Create your NFC cards

Burning attack cards

```
cd $PCO_BASE/nfc/py/pokemon/util/
python burnattack.py <attack number>
```

```
cd $PCO_BASE/nfc/py/pokemon/util/
python burnpokemon.py <pokemon number>
```
