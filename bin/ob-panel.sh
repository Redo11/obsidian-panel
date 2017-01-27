#!/bin/sh
### BEGIN INIT INFO
# Provides:          ob-panel
# Required-Start:    $local_fs $network $named $time $syslog
# Required-Stop:     $local_fs $network $named $time $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       This is an Minecraft server manageer
### END INIT INFO

DIR=$(dirname $([ -L $0 ] && readlink -f $0 || echo $0))

PIDFILE=/var/run/ob-panel.pid

_parse_yaml() {
   local prefix=$2
   local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @|tr @ '\034')
   sed -ne "s|^\($s\)\($w\)$s:$s\"\(.*\)\"$s\$|\1$fs\2$fs\3|p" \
        -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p"  $1 |
   awk -F$fs '{
      indent = length($1)/2;
      vname[indent] = $2;
      for (i in vname) {if (i > indent) {delete vname[i]}}
      if (length($3) > 0) {
         vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
         printf("%s%s%s=\"%s\"\n", "'$prefix'",vn, $2, $3);
      }
   }'
}

_start_circus(){
    echo "[INFO] Start Obsidian Panel LEVEL - 2"
    circusd --pidfile $PIDFILE .obsidian_panel.ini --daemon
}

cmd_circusctl(){
    eval $(_parse_yaml $(dirname "$DIR")/config.yaml "config_")
    circusctl --endpoint=tcp://127.0.0.1:$config_circus_end_port --timeout 3 $@
}

start(){
    echo "Start obsidian-panel..."
    sh $DIR/gen.circus.sh
    cd $DIR/../
    if [ ! -f $PIDFILE ]; then
        _start_circus
    else
        echo "[INFO] Start Obsidian Panel LEVEL - 1"
    fi
    cmd_circusctl start
}

status(){
    cmd_circusctl status
}

stop(){
    echo "Stop obsidian-panel..."
    kill -2 $(cat $PIDFILE)
    rm -f $PIDFILE
}

clear(){
    echo "Unimplemented."
}

restart(){
    echo "Restart obsidian-panel..."
    # generate ini file
    sh $DIR/gen.circus.sh
    cd $DIR/../
    if [ ! -f $PIDFILE ]; then
        _start_circus
    else
        kill -2 $(cat $PIDFILE)
        rm -f $PIDFILE
        _start_circus
    fi
}

debug(){
    echo "Running in debug mode..."

    if [ -f $PIDFILE ]; then
        quit
    fi
    # generate ini file
    sh $DIR/gen.circus.sh true
    cd $DIR/../
    circusd .obsidian_panel.ini
}

quit(){
    if [ -f $PIDFILE ]; then
        echo "Quit circus..."
        cmd_circusctl quit
        rm -f $PIDFILE
    fi
}

upgrade(){
    echo "[INFO] Update Obsidian-panel..."
    # change to the root directory.
    # ** by default, it is /opt/obsidian-panel (Linux)
    cd $DIR/../

    # set temperal username and email
    # or `git pull` operation will not continue
    git config user.name obuser
    git config user.email obuser@obuser.com

    # now pull the code from upstream
    if git pull -f --no-edit origin master; then
        echo "[INFO] Update succeed. New version is $(cat $DIR/../VERSION)"
        exit 0
    else
        echo "[INFO] Update failed."
        exit 1
    fi
}

# dev command
dev(){
    case "$1" in
        publish)
            dev_publish
            ;;
        push)
            dev_push
            ;;
        *)
            ;;
    esac
}

dev_publish(){
    dev_push
    echo "[INFO] publish changes"
    git checkout master
    git merge dev
    git tag -a $(cat $DIR/../VERSION)
    git push origin master
    git push mirror master
}

dev_push(){
    echo "[INFO] push updates"
    echo "[INFO] NOTICE: Before upload changes to upstream, you should commit all the changes"
    # push to GitHub
    git push origin dev
    # push to coding.net (China mirror)
    git push mirror dev
}

# command switch
case "$1" in
  start)
      start
      ;;
  stop)
      stop
      ;;
  clear)
      clear
      ;;
  dev)
      dev $2
      ;;
  restart)
      restart
      ;;
  status)
      status
      ;;
  debug)
      debug
      ;;
  quit)
      quit
      ;;
  upgrade)
      upgrade
      ;;
  update)
      upgrade
      ;;
  *)
    echo "Usage: $0 {start|stop|restart|status|clear|debug|quit|upgrade|update}"
esac
