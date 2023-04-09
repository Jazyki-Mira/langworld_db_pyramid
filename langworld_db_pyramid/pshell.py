from langworld_db_pyramid import models


def setup(env):  # type: ignore
    request = env["request"]

    # start a transaction
    request.tm.begin()

    # inject some vars into the shell builtins
    env["tm"] = request.tm
    env["dbsession"] = request.dbsession
    env["models"] = models
