# Site tools

The pages are generated. Edit `tools/plugins.py` (the plugin catalogue) or `tools/style.css`, then run
`tools/assemble.sh` from a machine with `gh` signed in: it copies each plugin's display art and screenshots into
`images/plugins/<slug>/` and rebuilds `index.html` and `plugins/*.html`.

- Add a plugin: add an entry to `PLUGINS` in `plugins.py`.
- Add a feature video: put the file in `videos/<slug>/` and add its name as the third item of that feature,
  e.g. `("Eight modes", "JET is ...", "modes.mp4")`.
- Screenshots: `tools/shots.sh <repo> ...` builds each plugin's Shot tool (needs JUCE at /home/user/JUCE) and
  writes PNGs to /home/user/shots/<repo>; `assemble.sh` picks them up.
