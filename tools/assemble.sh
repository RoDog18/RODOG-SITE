#!/bin/bash
# Copies display art and screenshots into the site, then builds the pages.
site=/home/user/rodog-site
python3 -I -c "
import sys; sys.path.insert(0,'/home/user/rodog-site/tools')
from plugins import PLUGINS
for p in PLUGINS: print(p['slug'], p['repo'], *p['art'])
" | while read slug repo arts; do
  dst=$site/images/plugins/$slug; mkdir -p $dst
  for a in $arts; do
    [ -f $dst/$a ] || gh api repos/RoDog18/$repo/contents/Resources/images/$a -H "Accept: application/vnd.github.raw" > $dst/$a
  done
  if [ -d /home/user/shots/$repo ]; then
    for f in /home/user/shots/$repo/*.png; do
      b=$(basename $f); case $b in *presets*|frame-*) continue;; esac
      n=$dst/shot-${b%.png}.jpg
      [ $f -nt $n ] && python3 -I -c "
from PIL import Image; im=Image.open('$f').convert('RGB'); im.thumbnail((1600,1600)); im.save('$n', quality=85, optimize=True)"
    done
  fi
done
cp /home/user/rodog-site/tools/style.css /home/user/rodog-site/tools/site.js $site/
python3 -I /home/user/rodog-site/tools/build.py $site
