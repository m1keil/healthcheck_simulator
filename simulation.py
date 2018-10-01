import simpy
import random


INTERVAL = 30
HEALTHY_THRESHOLD = 10
UNHEALTHY_THRESHOLD = 2
#GRACE_PERIOD = 600
SUCCESS_RATE = 80

HEALTHY = True
UNHEALTHY = False
OK = True
ERR = False


def healthcheck(env):
    state = UNHEALTHY
    last_check = False
    c = 0

    while True:
        check_result = check(SUCCESS_RATE)
        print(f'{env.now}: current state: {state}, healthcheck result: {check_result}')

        if check_result == last_check:
            c += 1
        else:
            c = 1
        last_check = check_result

        if state is HEALTHY and check_result is ERR and c == UNHEALTHY_THRESHOLD:
                state = UNHEALTHY
                print(f'{env.now}: changing state to UNHEALTHY')

        if state is UNHEALTHY and check_result is OK and c == HEALTHY_THRESHOLD:
                state = HEALTHY
                print(f'{env.now}: changing state to HEALTHY')

        yield env.timeout(INTERVAL)


def check(success):
    return random.choices([OK, ERR], weights=[success, 100-success])[0]


env = simpy.Environment()
p = env.process(healthcheck(env))
env.run(3600)

