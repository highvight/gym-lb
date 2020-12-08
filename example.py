import gym

# Check for root privileges
euid = os.geteuid()
if euid != 0:
  raise EnvironmentError("Failed. You need to be root")
  exit()

env = gym.make('gym_lb:lb-v0')

# An action is a list of weights for the ipvs scheduler
action = [1,1,1]
state, result, finished, info = env.step(action)
print("##### RESULT 1 #######")
print(state)
print(result)
print("######################")

action = [5,1,1]
state, result, finished, info = env.step(action)
print("##### RESULT 2 #######")
print(state)
print(result)
print("######################")

action = [1,5,1]
state, result, finished, info = env.step(action)
print("##### RESULT 3 #######")
print(state)
print(result)
print("######################")

action = [1,1,5]
state, result, finished, info = env.step(action)
print("##### RESULT 4 #######")
print(state)
print(result)
print("######################")

