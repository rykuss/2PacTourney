# Pacman Capture the Flag: Team 2Pac

This branch is for testing the newly added smart power capsule ally retrieval and smart invader pinning (for handling multiple invaders). Food prioritization with decreasing game time is also included in this branch but commented out (couldn't get it working correctly). 

## Bugs
### Scenario 1: 
Running `python capture.py -r myTeam -b baselineTeam` with `OffensiveReflexAgent` and `DefensiveReflexAgent`

* Defenders run away from invader when they're not in fact scared. Maybe this has something to do with trying to pin the invader?
	* Observed on `-l` (layout) `RANDOM7, RANDOM17, RANDOM20, RANDOM22`
* Our invader freezes next to enemy defender
	* Observed on `-l` (layout) `RANDOM26, RANDOM35`

### Scenario 2:
Running `python capture.py -r myTeam -b baselineTeam` with `OffensiveReflexAgent` and `OffensiveReflexAgent`
* Defending agent tries to pin both enemy invaders but does not even eat either of them
	* Observed on `-l` (layout) `RANDOM1, RANDOM3, RANDOM9, RANDOM14, RANDOM25, RANDOM26`
* Defending agent pins invader, `"Close!!!!"` is printed when other enemy invader is near, yet doesn't eat current pinned invader
	* Observed on `-l` (layout) `RANDOM15`
* Both invader agents avoid a power capsule when right next to an enemy defender ghost and get eaten
	* Observed on `-l` (layout) `RANDOM20`
* Exception thrown [Observed on `-l` (layout) `RANDOM16, RANDOM30`]:

```
Traceback (most recent call last):
  File "capture.py", line 833, in <module>
    runGames(**options)
  File "capture.py", line 794, in runGames
    g.run()
  File "C:\Users\yona.edell\Documents\CS140\Tournament\game.py", line 662, in run
    action = agent.getAction(observation)
  File "C:\Users\yona.edell\Documents\CS140\Tournament\captureAgents.py", line 156, in getAction
    return self.chooseAction(gameState)
  File "C:\Users\yona.edell\Documents\CS140\Tournament\myTeam.py", line 58, in chooseAction
    values[a] = self.evaluate(gameState, a)
  File "C:\Users\yona.edell\Documents\CS140\Tournament\myTeam.py", line 86, in evaluate
    return self.getValue(gameState, action)
  File "C:\Users\yona.edell\Documents\CS140\Tournament\myTeam.py", line 277, in getValue
    if self.getMazeDistance(successor.getAgentState(allyIndex).getPosition(), d.getPosition()) > dists:  # Check if ally is further from ghost than current agent
  File "C:\Users\yona.edell\Documents\CS140\Tournament\captureAgents.py", line 241, in getMazeDistance
    d = self.distancer.getDistance(pos1, pos2)
  File "C:\Users\yona.edell\Documents\CS140\Tournament\distanceCalculator.py", line 38, in getDistance
    if isInt(pos1) and isInt(pos2):
  File "C:\Users\yona.edell\Documents\CS140\Tournament\distanceCalculator.py", line 65, in isInt
    x, y = pos
TypeError: 'NoneType' object is not iterable
```

## A few handy commands:
* Run a basic game
  * `python capture.py`
* Run game with specified Red and Blue teams (baselineTeam shown here for both)
  * `python capture.py -r baselineTeam -b baselineTeam`
* Run game controlling agent0 with arrowkeys and specified amount of time
  * `python capture.py --keys0 -i <time_amount>`
* Run game with specified layout
  * `python capture.py -l <layout_file>`
    * Use `-l RANDOM0` for a random maze layout
    * Use `-l RANDOM<seed_num>` for a specified random seed layout
* Run game replay from .rec file
  * `python capture.py --replay=<filename.rec>`
* Run game with no graphics and minimal output
  * `python capture.py -q`
* Run game with specified number of games
  * `python capture.py -n <num_games>`
* Run game with fixed random seed to always play the same game
  * `python capture.py -f`
