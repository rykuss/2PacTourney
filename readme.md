# Pacman Capture the Flag: Team 2Pac

A few handy commands:
* Run a basic game
  * `python capture.py`
* Run game with specified Red and Blue teams (baselineTeam shown here for both)
  * `python capture.py -r baselineTeam -b baselineTeam`
* Run game controlling agent0 with arrowkeys and specified amount of time
  * `python capture.py --keys0 -i <time_amount>`
* Run game with specified layout
  * `python capture.py -l <layout_file>`
    * Use `-l RANDOM` for a random maze layout
    * Use `-l RANDOM<seed_num>` for a specified random seed layout
* Run game replay from .rec file
  * `python capture.py --replay=<filename.rec>`
* Run game with no graphics and minimal output
  * `python capture.py -q`
* Run game with specified number of games
  * `python capture.py -n <num_games>`
* Run game with fixed random seed to always play the same game
  * `python capture.py -f`
