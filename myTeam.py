# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DummyAgent', second = 'DummyAgent'):
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

<<<<<<< Updated upstream
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

=======
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

    maxValue = -100000
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

    # Initialization
    successor = self.getSuccessor(gameState, action)
    value = 0.0
    myPos = successor.getAgentState(self.index).getPosition()

    # ***** BEGIN Food & Score Tallying *****

    foodList = self.getFood(successor).asList()   # Compute distance to the nearest food
    if len(foodList) > 0: # This should always be True, but better safe than sorry
      midHeightFood = (gameState.data.food.height) / 2
      closestUpperFood = 100.0
      closestBelowFood = 100.0
      for food in foodList:
        if food[1] >= midHeightFood:                # Check y value of tuple
          dists = self.getMazeDistance(myPos, food) # Get distance between successor position and food
          if dists < closestUpperFood:
            closestUpperFood = dists                # Closest upper food updated with correct distance
        elif food[1] < midHeightFood:               # Check y value of tuple
          dists = self.getMazeDistance(myPos, food)
          if dists < closestBelowFood:
            closestBelowFood = dists                # Closest lower food updated with correct distance
      value += (((1.0/(closestUpperFood+1.0)) * 102.0) + ((1.0/(closestBelowFood+1.0)) * 30.0))  # AgentOne prefers upper grid while AgentTwo prefers lower food
                                                                                                 # TODO: Reconfigure reciprocals to negatives
      value += self.getScore(successor)*100.0       # Value score to encourage eating food you're immediately next to

    # ***** BEGIN Ghost/Capsule accounting when agent is invader *****

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]  # Get opponent states
    if successor.getAgentState(self.index).isPacman:                              # Check if AgentOne is Pacman
      defenders = [a for a in enemies if not a.isPacman and a.getPosition() != None]  # Get opponent defenders within 5 distance
      for d in defenders:
        dists = self.getMazeDistance(myPos, d.getPosition())  # For every enemy defender, calculate distance between agent next position and enemy current position
        if d.scaredTimer == 0:                                # Check if enemy defender is not scared

          value -= ((1.0/(dists+1)) * 200.0)  # Discourage current agent travel towards defender ghost

          capsuleList = self.getCapsules(gameState)
          closestCapDist = min([self.getMazeDistance(myPos, cap) for cap in capsuleList])  # Calculate distance between you and closest capsule

          allyIndex = -1  # Find index of other agent on team
          if self.index == 0:
            allyIndex = 2
          elif self.index == 1:
            allyIndex = 3
          if len(capsuleList) > 0: # If capsules are available
            if successor.getAgentState(allyIndex).isPacman:  # Check if ally is pacman
              if self.getMazeDistance(successor.getAgentState(allyIndex).getPosition(), d.getPosition()) > dists:  # Check if ally is further from ghost than current agent
                value -= ((1.0 / (dists + 1)) * 100.0)  # Discourage current agent travel towards defender ghost EVEN MORE
                value +=((1.0/(closestCapDist+1)) * 20.0) # If we happen to come by a capsule along our running away, eat the capsule
              else:
                value +=((1.0/(closestCapDist+1)) * 100.0)
          # TODO: Copy this into other agent so it will also account


          # value += ((1.0/(closestCapDist+1)) * 30.0) # Encourage pacman to visit closest capsule while ghost is close and not scared

        elif d.scaredTimer > 10:
          if dists < 6:   # If distance between current agent and now scared ghost is less than 6
            value -= ((1.0/(dists+1)) * 100.0)  # Discourage travel toward scared ghost
        elif d.scaredTimer <= 10: # Check if ghost scared timer is about to expire
          if dists < 6:           # If scared ghost is within range, go toward it and eat it
            value += ((1.0/(dists+1)) * 412.0)  #

    # ***** END Ghost/Capsule accounting *****

    # ***** BEGIN Accounting for invaders within sight *****

    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None] # Get opponent invaders within 5 distance
    if successor.getAgentState(self.index).scaredTimer == 0:  # Check if current agent is not scared (as a ghost)
      for i in invaders:
        dists = self.getMazeDistance(myPos, i.getPosition())  # Distance between current agent and i invader
        if dists < 6:
          allyIndex = -1                                      # Find index of other agent on team
          if self.index == 0:
            allyIndex = 2
          elif self.index == 1:
            allyIndex = 3

          # Distance between i invader and ally
          distsAlly = self.getMazeDistance(successor.getAgentState(allyIndex).getPosition(), i.getPosition())

          if distsAlly > 1: # Check if invader is more than 1 distance away from ally
            if self.getScore(successor) >= -3:     # Check if successor score is not currently losing by more than 3
              value += ((1.0/(dists+1)) * 40004.0) # We can afford to pin i invader/allow pinning
            else:                                  # Losing by more than 3,
              value += ((1.0/(dists+1)) * 4004.0)  # Encourages eating of i invader so we can use this agent to collect food on other side

            value -= (len(invaders)*4000)  # Lets agent eat i invader if losing by >3
            # TODO: Check if there is another invader that comes by, so we either keep pinning current invader or eat them and get the new invader
    elif successor.getAgentState(self.index).scaredTimer > 0:  # If current agent is scared
      for i in invaders:
        dists = self.getMazeDistance(myPos, i.getPosition())   # Distance between current agent and i invader
        if dists < 6:
          value -= ((1.0/(dists+1)) * 60.0)                    # Discourage travel to i invader

    # ***** END Accounting for invaders within sight *****

    # TODO: Account for invaders that are out of sight/disregard if this agent is a pacman/invader


    return value

class OffensiveReflexAgentTwo(ReflexCaptureAgent):

  def getValue(self, gameState, action):

    # Initialization
    successor = self.getSuccessor(gameState, action)
    value = 0.0
    myPos = successor.getAgentState(self.index).getPosition()

    # ***** BEGIN Food & Score Tallying *****

    foodList = self.getFood(successor).asList()   # Compute distance to the nearest food
    if len(foodList) > 0: # This should always be True, but better safe than sorry
      midHeightFood = (gameState.data.food.height) / 2
      closestUpperFood = 100.0
      closestBelowFood = 100.0
      for food in foodList:
        if food[1] >= midHeightFood:                # Check y value of tuple
          dists = self.getMazeDistance(myPos, food) # Get distance between successor position and food
          if dists < closestUpperFood:
            closestUpperFood = dists                # Closest upper food updated with correct distance
        elif food[1] < midHeightFood:               # Check y value of tuple
          dists = self.getMazeDistance(myPos, food)
          if dists < closestBelowFood:
            closestBelowFood = dists                # Closest lower food updated with correct distance
      value += (((1.0/(closestUpperFood+1.0)) * 30.0) + ((1.0/(closestBelowFood+1.0)) * 102.0))  # AgentTwo prefers lower grid while AgentOne prefers upper food
                                                                                                 # TODO: Reconfigure reciprocals to negatives
      value += self.getScore(successor)*100.0       # Value score to encourage eating food you're immediately next to

    # ***** BEGIN Ghost/Capsule accounting when agent is invader *****

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]  # Get opponent states
    if successor.getAgentState(self.index).isPacman:                              # Check if AgentOne is Pacman
      defenders = [a for a in enemies if not a.isPacman and a.getPosition() != None]  # Get opponent defenders within 5 distance
      for d in defenders:
        dists = self.getMazeDistance(myPos, d.getPosition())  # For every enemy defender, calculate distance between agent next position and enemy current position
        if d.scaredTimer == 0:                                # Check if enemy defender is not scared

          value -= ((1.0/(dists+1)) * 200.0)  # Discourage current agent travel towards defender ghost

          capsuleList = self.getCapsules(gameState)
          closestCapDist = min([self.getMazeDistance(myPos, cap) for cap in capsuleList])  # Calculate distance between you and closest capsule

          allyIndex = -1  # Find index of other agent on team
          if self.index == 0:
            allyIndex = 2
          elif self.index == 1:
            allyIndex = 3
          if len(capsuleList) > 0: # If capsules are available
            if successor.getAgentState(allyIndex).isPacman:  # Check if ally is pacman
              if self.getMazeDistance(successor.getAgentState(allyIndex).getPosition(), d.getPosition()) > dists:  # Check if ally is further from ghost than current agent
                value -= ((1.0 / (dists + 1)) * 100.0)  # Discourage current agent travel towards defender ghost EVEN MORE
                value +=((1.0/(closestCapDist+1)) * 20.0) # If we happen to come by a capsule along our running away, eat the capsule
              else:
                value +=((1.0/(closestCapDist+1)) * 100.0)
          # TODO: Copy this into other agent so it will also account


          # value += ((1.0/(closestCapDist+1)) * 30.0) # Encourage pacman to visit closest capsule while ghost is close and not scared

        elif d.scaredTimer > 10:
          if dists < 6:   # If distance between current agent and now scared ghost is less than 6
            value -= ((1.0/(dists+1)) * 100.0)  # Discourage travel toward scared ghost
        elif d.scaredTimer <= 10: # Check if ghost scared timer is about to expire
          if dists < 6:           # If scared ghost is within range, go toward it and eat it
            value += ((1.0/(dists+1)) * 412.0)  #

    # ***** END Ghost/Capsule accounting *****

    # ***** BEGIN Accounting for invaders within sight *****

    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None] # Get opponent invaders within 5 distance
    if successor.getAgentState(self.index).scaredTimer == 0:  # Check if current agent is not scared (as a ghost)
      for i in invaders:
        dists = self.getMazeDistance(myPos, i.getPosition())  # Distance between current agent and i invader
        if dists < 6:
          allyIndex = -1                                      # Find index of other agent on team
          if self.index == 2:
            allyIndex = 0
          elif self.index == 3:
            allyIndex = 1

          # Distance between i invader and ally
          distsAlly = self.getMazeDistance(successor.getAgentState(allyIndex).getPosition(), i.getPosition())

          if distsAlly > 1: # Check if invader is more than 1 distance away from ally
            if self.getScore(successor) >= -3:     # Check if successor score is not currently losing by more than 3
              value += ((1.0/(dists+1)) * 40004.0) # We can afford to pin i invader/allow pinning
            else:                                  # Losing by more than 3,
              value += ((1.0/(dists+1)) * 4004.0)  # Encourages eating of i invader so we can use this agent to collect food on other side

            value -= (len(invaders)*4000)  # Lets agent eat i invader if losing by >3
            # TODO: Check if there is another invader that comes by, so we either keep pinning current invader or eat them and get the new invader
    elif successor.getAgentState(self.index).scaredTimer > 0:  # If current agent is scared
      for i in invaders:
        dists = self.getMazeDistance(myPos, i.getPosition())   # Distance between current agent and i invader
        if dists < 6:
          value -= ((1.0/(dists+1)) * 60.0)                    # Discourage travel to i invader

    # ***** END Accounting for invaders within sight *****

    # TODO: Account for invaders that are out of sight/disregard if this agent is a pacman/invader


    return value
>>>>>>> Stashed changes
