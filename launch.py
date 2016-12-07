__author__ = "Nigshoxiz"

# Dev Note:
# For some strange reasons, it is not allowed to run a chaussette instance
# using eventlet backend in python3 (chaussette version: v0.13.0, which is the newest version pip could download).
# That is, we can't run `chaussette run.app --backed eventlet` to start server directly.
# In fact, chaussette supports eventlet backend in python3 internally, it just denies `eventlet` as an option
# of `--backend` in command line. Considering the stability of eventlet library in python3, which has been
# improved a lot since the release date of chaussette v0.13.0 (2015), we monkey-patch it to bypass the
# restriction of command line .
#
# And How to run in circus?
#
# Just append the following configuration:
#
# [watcher:xxx]
# cmd = python start_chaussette.py --fd $(circus.sockets.web)
#
# Nigshoxiz
# 2016-8-16

import sys, getopt

def start_chaussette(use_reloader):
    from app import app as _app
    from app import logger
    from app.controller.global_config import GlobalConfig
    from app.controller.init_main_db import init_database

    from chaussette.backend import _backends
    from chaussette.backend._eventlet import Server as eventlet_server
    from chaussette.server import make_server

    import os
    _host = "fd://%d" % int(sys.argv[4])

    logger.debug("This is Main Server (%s)" % os.getpid())
    def init_directory():
        gc = GlobalConfig.getInstance()
        dirs = [
            gc.get("base_dir"),
            gc.get("uploads_dir"),
            gc.get("files_dir"),
            gc.get("servers_dir"),
            gc.get("lib_bin_dir"),
            gc.get("sqlite_dir")
        ]

        for item in dirs:
            if not os.path.isdir(item):
                os.makedirs(item)

    def _make_server():
        try:
            # instill eventlet_server instance to `_backends` dict to bypass the restriction!
            _backends['eventlet'] = eventlet_server
            httpd = make_server(_app, host=_host,
                                backend='eventlet')

            httpd.serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)

    # init directories
    init_directory()

    # init database
    init_database(logger=logger)

    if use_reloader:
        try:
            from werkzeug.serving import run_with_reloader
        except ImportError:
            logger.info("Reloader requires Werkzeug: "
                        "'pip install werkzeug'")
            sys.exit(0)
        run_with_reloader(_make_server)
    else:
        _make_server()

def start_ftp_manager():
    from ftp_manager import start_FTP_manager
    start_FTP_manager()

def start_websocket_server():
    from websocket_server import start_websocket_server
    start_websocket_server()

def start_process_watcher():
    '''
    from process_watcher.watchdog import Watchdog
    from process_watcher.mq_events import EventSender, WatcherEvents
    from process_watcher.mq_proxy import MessageQueueProxy

    watcher = Watchdog.getWDInstance()
    watcher.launch(hook_class=EventSender)
    # init recv events
    proxy = MessageQueueProxy.getInstance()
    WatcherEvents()
    proxy.listen()
    '''
    from process_watcher import start_process_watcher
    start_process_watcher()

try:
    opts, args = getopt.getopt(sys.argv[1:], "b:p:d", ["debug", "use_reloader"])
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

debug_flag = False
listen_port = None
branch_name = None
use_reloader = False
# parse args
for o, a in opts:
    if o == "-b":
        branch_name = a
    elif o == "-d":
        debug_flag = True
    elif o == "-p":
        listen_port = int(a)
    elif o == "--use_reloader":
        if a == "true":
            use_reloader = True
        else:
            use_reloader = False
    elif o == "--debug":
        if a == "true":
            debug_flag = True
        else:
            debug_flag = False

# TODO: add params
if launch_branch_name == "app":
    start_chaussette(False)
elif launch_branch_name == "ftp_manager":
    start_ftp_manager()
elif launch_branch_name == "process_watcher":
    start_process_watcher()
elif launch_branch_name == "websocket_server":
    start_websocket_server()
