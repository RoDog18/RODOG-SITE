# Site tools

The pages are generated. Edit `tools/plugins.py` (the plugin catalogue) or `tools/style.css`, then run
`tools/assemble.sh` from a machine with `gh` signed in: it copies each plugin's display art and screenshots into
`images/plugins/<slug>/` and rebuilds `index.html` and `plugins/*.html`.

- Add a plugin: add an entry to `PLUGINS` in `plugins.py`.
- Feature pictures: by default each feature shows a screenshot whose file name matches a word in its title.
  To pick one, add its file name as the third item, e.g. `("Eight modes", "JET is ...", "shot-fanger-swarm.jpg")`.
- The walkthrough video sits above the Features section (placeholder until a video is added).
- Screenshots: `tools/shots.sh <repo> ...` builds each plugin's Shot tool (needs JUCE at /home/user/JUCE) and
  writes PNGs to /home/user/shots/<repo>; `assemble.sh` picks them up.
