if [ -x /sbin/setcap ]; then
  bin=(jackdbus jackd jack_control)

  for i in ${bin[@]}; do
    /sbin/setcap cap_ipc_lock,cap_sys_nice=ep usr/bin/$i
  done
fi
