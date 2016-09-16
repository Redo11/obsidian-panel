__author__ = "Nigshoxiz"

from . import event_loop, logger, SERVER_STATE
from .instance import MCServerInstance
from .mc_config import MCWrapperConfig
import threading

POLL_NULL = 0x00
POLL_IN = 0x01
POLL_OUT = 0x04
POLL_ERR = 0x08
POLL_HUP = 0x10
POLL_NVAL = 0x20

class Watchdog(object):
    instance = None

    def __init__(self):
        '''process pool stores the instance object
        KEY -> "inst_" + <inst id>
        VALUE -> {
            "config" : MC config obj,
            "port" : MC listening port,
            "inst" : MC inst obj,
            "log" : MC running log [array]
        }
        '''
        self.proc_pool = {}
        pass

    @staticmethod
    def getWDInstance():
        if Watchdog.instance == None:
            Watchdog.instance = Watchdog()
        return Watchdog.instance

    def _handle_log(self, events):
        for sock, fd, event in events:
            if event == POLL_IN:
                if sock.closed == False:
                    # get sender by comparing output fd
                    for inst_key in self.proc_pool:
                        inst_obj = self.proc_pool.get(inst_key)
                        _inst = inst_obj["inst"]

                        if fd == _inst._proc.stdout.fileno():
                            log_str = _inst._proc.stdout.read(512)
                            log_arr = log_str.decode('utf-8').split("\n")
                            # append log
                            inst_obj["log"] += log_arr
                else:
                    logger.warning("pipe socket is closed!")
            else:
                # TODO
                pass

    def register_instance(self, inst_id, port, config):
        '''
        register a new instance to the process pool, which manages all minecraft processes.
        :param inst_id:
        :param port:
        :param config:
        :return:
        '''
        _port = int(port)
        _inst_key = "inst_" + str(inst_id)
        _inst_val = {
            "config" : MCWrapperConfig(**config), # READ_ONLY
            "port" : _port, # READ_ONLY
            "inst" : None, #MCServerInstance(_port),
            "log" : []
        }

        _k = self.proc_pool.get(_inst_key)
        print(_k)
        if _k != None:
            if _k.get("inst") == None:
                _k["inst"] = MCServerInstance(_port)
        else:
            self.proc_pool[_inst_key] = _inst_val
            self.proc_pool[_inst_key]["inst"] = MCServerInstance(_port)
        return True

    def add_instance(self, inst_id, port, config):
        '''
        just an alias of method `register_instance`
        '''
        return self.register_instance(inst_id, port, config)

    def del_instance(self, inst_id):
        '''
        Delete instance from the world.
        Be really CAREFUL, it may lost everything!
        :param inst_id:
        :return:
        '''
        _inst_key = "inst_" + str(inst_id)
        if self.proc_pool.get(_inst_key) != None:
            del self.proc_pool[_inst_key]

    def start_instance(self, inst_id):
        _inst_key = "inst_" + str(inst_id)
        _inst_conf = self.proc_pool.get(_inst_key)

        _inst = _inst_conf.get("inst")
        _config = _inst_conf.get("config")
        if _inst == None:
            raise Exception("Instance is None!")
        else:
            if _inst._status == SERVER_STATE.HALT:
                _inst.start_process(_config)

    def stop_instance(self, inst_id):
        _inst_key = "inst_" + str(inst_id)
        _inst_profile = self.proc_pool.get(_inst_key)

        _inst = _inst_profile.get("inst")
        if _inst == None:
            raise Exception("Instance is None!")
        else:
            if _inst._status == SERVER_STATE.RUNNING \
                    or _inst._status == SERVER_STATE.STARTING:
                # TODO
                _inst.stop_process()

    def get_instance(self, inst_id):
        _inst_key = "inst_" + str(inst_id)
        if self.proc_pool.get(_inst_key) == None:
            return None
        else:
            return self.proc_pool.get(_inst_key).get("inst")

    def launch(self):
        def _launch_loop():
            event_loop.run()

        # before start
        event_loop.add_handler(self._handle_log)
        event_loop.stopping = False
        t = threading.Thread(target=_launch_loop)
        t.daemon = True
        t.start()
        logger.info("start Watchdog thread.")

    def terminate(self):
        # set stopping to True -> terminate while loop
        event_loop.stopping = True
        logger.info("stop Watchdog thread.")