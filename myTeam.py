# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveReflexAgentOne', second = 'OffensiveReflexAgentTwo'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on). 
    
    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    ''' 
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py. 
    '''
    CaptureAgent.registerInitialState(self, gameState)

    ''' 
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    ''' 
    You should change this in your own agent.
    '''

    return random.choice(actions)


class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = util.Counter()
    for a in actions:
      values[a] = self.evaluate(gameState, a) 
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    if len(actions) > 1:
      print self.index
      print "ITERATION"
      for a in actions:
        print a
        print values[a]

    maxValue = -1000
    for a in actions:
      if maxValue < values[a]:
        maxValue = values[a]

    choices = []
    for a in actions:
      if values[a] == maxValue:
        choices.append(a)

    return random.choice(choices)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    return self.getValue(gameState, action)



class OffensiveReflexAgentOne(ReflexCaptureAgent):

  def getValue(self, gameState, action):
    successor = self.getSuccessor(gameState, action)
    value = 0.0
    myPos = successor.getAgentState(self.index).getPosition()
    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      midway = (gameState.data.food.height) / 2
      closestUpperFood = 100.0
      closestBelowFood = 100.0
      for food in foodList:
        if food[1] >= midway:
          dists = self.getMazeDistance(myPos, food)
          if dists < closestUpperFood:
            closestUpperFood = dists
        elif food[1] < midway:
          dists = self.getMazeDistance(myPos, food)
          if dists < closestBelowFood:
            closestBelowFood = dists
      value += (((1.0/(closestUpperFood+1.0)) * 102.0) + ((1.0/(closestBelowFood+1.0)) * 30.0))
      value += self.getScore(successor)*100.0

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    if successor.getAgentState(self.index).isPacman:
      defenders = [a for a in enemies if not a.isPacman and a.getPosition() != None]
      for d in defenders:
        dists = self.getMazeDistance(myPos, d.getPosition())
        if d.scaredTimer == 0:
          allyIndex = self.index
          if self.red:
            if self.index == 0:
              allyIndex = 2
            else:
              allyIndex = 0
          else:
            if self.index == 1:
              allyIndex = 3
            else:
              allyIndex = 1

          distsAlly = self.getMazeDistance(successor.getAgentState(allyIndex).getPosition(), d.getPosition())
          if dists < 4:
            value -= ((1.0/(dists+1)) * 200.0)
            capsuleList = self.getCapsules(gameState)
            if len(capsuleList) > 0: 
              dists = min([self.getMazeDistance(myPos, cap) for cap in capsuleList])
              value += ((1.0/(dists+1)) * 30.0)
          elif distsAlly < 4:
            capsuleList = self.getCapsules(gameState)
            if len(capsuleList) > 0: 
              dists = min([self.getMazeDistance(myPos, cap) for cap in capsuleList])
              value += ((1.0/(dists+1)) * 624.0)
        elif d.scaredTimer > 10:
          if dists < 4:
            value -= ((1.0/(dists+1)) * 100.0)
        elif d.scaredTimer <= 10:
          if dists < 4:
            value += ((1.0/(dists+1)) * 412.0)
    elif not successor.getAgentState(self.index).isPacman:
      invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
      myCurrentPos = gameState.getAgentState(self.index).getPosition()
      if successor.getAgentState(self.index).scaredTimer == 0:
        for i in invaders:
          dists = self.getMazeDistance(myCurrentPos, i.getPosition())
          if dists < 4:
            value += ((1.0/(dists+1)) * 204.0) 
      elif successor.getAgentState(self.index).scaredTimer > 0:
        for i in invaders:
          dists = self.getMazeDistance(myPos, i.getPosition())
          if dists < 3:
            value -= ((1.0/(dists+1)) * 60.0) 
    return value




class OffensiveReflexAgentTwo(ReflexCaptureAgent):

  def getValue(self, gameState, action):
    successor = self.getSuccessor(gameState, action)
    value = 0.0
    myPos = successor.getAgentState(self.index).getPosition()
    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      midway = (gameState.data.food.height) / 2
      closestUpperFood = 100.0
      closestBelowFood = 100.0
      for food in foodList:
        if food[1] >= midway:
          dists = self.getMazeDistance(myPos, food)
          if dists < closestUpperFood:
            closestUpperFood = dists
        elif food[1] < midway:
          dists = self.getMazeDistance(myPos, food)
          if dists < closestBelowFood:
            closestBelowFood = dists
      value += (((1.0/(closestUpperFood+1.0)) * 30.0) + ((1.0/(closestBelowFood+1.0)) * 102.0))
      value += self.getScore(successor)*100.0

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    if successor.getAgentState(self.index).isPacman:
      defenders = [a for a in enemies if not a.isPacman and a.getPosition() != None]
      for d in defenders:
        dists = self.getMazeDistance(myPos, d.getPosition())
        if d.scaredTimer == 0:
          allyIndex = self.index
          if self.red:
            if self.index == 0:
              allyIndex = 2
            else:
              allyIndex = 0
          else:
            if self.index == 1:
              allyIndex = 3
            else:
              allyIndex = 1

          distsAlly = self.getMazeDistance(successor.getAgentState(allyIndex).getPosition(), d.getPosition())
          if dists < 4:
            value -= ((1.0/(dists+1)) * 200.0)
            capsuleList = self.getCapsules(gameState)
            if len(capsuleList) > 0: 
              dists = min([self.getMazeDistance(myPos, cap) for cap in capsuleList])
              value += ((1.0/(dists+1)) * 30.0)
          elif distsAlly < 4:
            capsuleList = self.getCapsules(gameState)
            if len(capsuleList) > 0: 
              dists = min([self.getMazeDistance(myPos, cap) for cap in capsuleList])
              value += ((1.0/(dists+1)) * 624.0)
        elif d.scaredTimer > 10:
          if dists < 4:
            value -= ((1.0/(dists+1)) * 100.0)
        elif d.scaredTimer <= 10:
          if dists < 4:
            value += ((1.0/(dists+1)) * 412.0)
    elif not successor.getAgentState(self.index).isPacman:
      invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
      myCurrentPos = gameState.getAgentState(self.index).getPosition()
      if successor.getAgentState(self.index).scaredTimer == 0:
        for i in invaders:
          dists = self.getMazeDistance(myCurrentPos, i.getPosition())
          if dists < 4:
            value += ((1.0/(dists+1)) * 204.0) 
      elif successor.getAgentState(self.index).scaredTimer > 0:
        for i in invaders:
          dists = self.getMazeDistance(myPos, i.getPosition())
          if dists < 3:
            value -= ((1.0/(dists+1)) * 60.0) 
    return value
