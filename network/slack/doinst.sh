if [ -x /usr/bin/update-desktop-database ]; then
  /usr/bin/update-desktop-database -q usr/share/applications >/dev/null 2>&1
fi

(cd usr/bin ; ln -sf /usr/lib64/slack/slack )
