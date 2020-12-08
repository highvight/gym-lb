import time

import docker
from gnlpy import ipvs
import gym
from tcp_latency import measure_latency

import config


class LbEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.ipvsadm = ipvs.IpvsClient()
        self.docker_cli = docker.from_env()

        self.service = ipvs.Service({
            "vip": config.SERVICE_IP,
            "port": config.SERVICE_PORT,
            'proto': config.SERVICE_PROTOCOL,
            'sched': config.SERVICE_SCHED
        })
        self._create_service()

        self.dests = [ipvs.Dest({
            "ip": config.SERVER_SUBNET + str(i),
            "port": config.SERVER_PORT,
            "weight": 1,
            "fwd_method": 0}) for i in range(config.SERVER_N)]
        self._create_dests(config.SERVER_IMAGE)

    def step(self, action):
        assert(len(action) == len(self.dests))

        for dest, weight in zip(self.dests, action):
            self.ipvsadm.update_dest(
                vip=self.service.vip(),
                port=self.service.port(),
                rip=dest.ip(),
                rport=dest.port(),
                weight=weight,
                method=dest.fwd_method(),
            )
        time.sleep(1)
        latency = measure_latency(host=self.service.vip(), port=self.service.port(), runs=50, wait=0.1, timeout=1, human_output=False)
        mean_latency = sum(latency)/len(latency)
        dests = self.ipvsadm.get_dests(self.service.to_attr_list())
        weights = [dest.weight() for dest in dests]

        return weights, mean_latency, False, dests

    def reset(self):
        for dest in self.dests:
            self.ipvsadm.update_dest(
                vip=self.service.vip(),
                port=self.service.port(),
                rip=dest.ip(),
                rport=dest.port(),
                weight=1,
                method=dest.fwd_method(),
            )
        dests = self.ipvsadm.get_dests(self.service.to_attr_list())
        weights = [dest.weight() for dest in dests]
        return weights


    def render(self, mode='human'):
        dests = self.ipvsadm.get_dests(self.service.to_attr_list())
        return dests

    def close(self):
        return

    def _create_service(self):
        '''Creates a service for load balancing.
        '''

        try:
            self.ipvsadm.del_service(vip=self.service.vip(), port=self.service.port())
            print("Service already present. Delete old service and create new one.")
        except Exception:
            print("Create Service.")
        self.ipvsadm.add_service(vip=self.service.vip(), port=self.service.port(), sched_name="wrr")
        return

    def _create_dests(self, image):
        '''Starts n container and links them to the service.
        '''
        for i, dest in enumerate(self.dests):
            container_name = "lb" + str(i)
            print("Spinning up server at: " + dest.ip())
            try:
                container = self.docker_cli.containers.get(container_name)
                print("Removing container" + container_name)
                container.stop()
                container.remove()
            except Exception:
                print("No container to remove")

            print("Running container" + container_name)
            self.docker_cli.containers.run(
                name=container_name,
                image=image,
                ports={80: (dest.ip(), dest.port())},
                detach=True
            )

            # Add Destinations to the service (rip = real ip address)
            self.ipvsadm.add_dest(
                vip=self.service.vip(),
                port=self.service.port(),
                rip=dest.ip(),
                rport=dest.port(),
                weight=dest.weight(),
                method=dest.fwd_method(),
            )
        return

    def _pull_image(self, image_name):
        ''' Pulls server image from DokerHub.
        '''

        self.docker_cli.images.pull(image_name)

        return
