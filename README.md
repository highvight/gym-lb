# gym-lb
A gym environment for load balancing

## TODO
- [ ] Docker container cpu and memory management (perhaps also network bandwith?)
- [ ] Fix gnlpy key error (for manual fix see below)
- [ ] Find good tool for latency measurement that works in Python (without cli)
- [ ] Upload to pip

## Installation
Clone this repo:

```
git clone https://github.com/highvight/rl-load-balancer.git
```

Install the package with:

```
pip install -e gym-lb
```

**Important**:

Most likely, you will run into some KeyErrors with `gnlpy` when running the gym environment. To fix this, you need to catch the KeyErrors in `gnlpy/netlink.py` like this:

```
...
(line 270)
try:
    if key_to_packer[k] == RecursiveSelf:
        v = AttrListType.unpack(data[4:alen])
    else:
        v = key_to_packer[k].unpack(data[4:alen])
except KeyError:
    return attr_list
...
```


### Requirements
A Linux machine with [ipvsadm](http://kb.linuxvirtualserver.org/wiki/Ipvsadm) and [Docker](https://www.docker.com/) installed.

For Debian-based distros get them with:

```
sudo apt-get install ipvsadm docker
```

## Usage
Start ipvsadm
```
sudo ipvsadm
```

In your code, create the environment with:
```
env = gym.make('gym_lb:lb-v0')
```

You need to run your script with root privileges. One option is:
```
sudo PYTHONPATH your_script.py #(or just use example.py)
```
where ```PYTHONPATH``` points to the python installation you want to use. For instance, if you use Anaconda, your path will look something like this: ```~/anaconda3/envs/ENVIRONMENT/bin/python```.

**Note**: You need to run the server management with root privileges. However, switching the user to root also switches the context in which you run python. Therefore, you need to explicitly point to the python path of the environment you want to use.

It is useful to check ipvsadm from console from time to time. Here are some useful commands:

```
sudo ipvsadm -l -n    # List all services and connected servers
sudo ipvsadm -C       # Clear the complete IPVS table
```
