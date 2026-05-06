# Active font profile is recorded in this state file (preserved across
# upgradepkg). Falls back to the build-time default if absent.
STATE=opt/Signal/resources/.active-profile

if [ -r "$STATE" ]; then
  profile=$(cat "$STATE")
else
  profile="@@FONT_PROFILE@@"
fi

if [ ! -f "opt/Signal/resources/app.asar.${profile}" ]; then
  profile="@@FONT_PROFILE@@"
fi

cp -fp "opt/Signal/resources/app.asar.${profile}" opt/Signal/resources/app.asar
echo "$profile" > "$STATE"

if [ -x /usr/bin/update-desktop-database ]; then
  /usr/bin/update-desktop-database -q usr/share/applications >/dev/null 2>&1
fi

if [ -e usr/share/icons/hicolor/icon-theme.cache ]; then
  if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -f usr/share/icons/hicolor >/dev/null 2>&1
  fi
fi
