#!/bin/bash
# Builds each plugin's Shot tool and saves its screenshots to /home/user/shots/<repo>
for r in "$@"; do
  d=/home/user/src/$r; o=/home/user/shots/$r; mkdir -p $o /home/user/src
  [ -d $d/.git ] || git clone -q --depth 1 https://github.com/RoDog18/$r $d || { echo "$r: clone failed"; continue; }
  if ! grep -q PLUGIN_SHOTS $d/CMakeLists.txt; then echo "$r: no shot tool"; continue; fi
  ( cd $d && cmake -B sbuild -G Ninja -DCMAKE_BUILD_TYPE=Release -DJUCE_DIR=/home/user/JUCE -DPLUGIN_FORMATS=VST3 -DPLUGIN_SHOTS=ON > /home/user/src/$r-cfg.log 2>&1 \
    && cmake --build sbuild --target Shot -j4 > /home/user/src/$r-build.log 2>&1 ) || { echo "$r: build failed"; continue; }
  bin=$(find $d/sbuild -type f -name Shot -perm -u+x | head -1)
  mkdir -p /home/user/src/home-$r
  ( cd $o && HOME=/home/user/src/home-$r timeout 300 "$bin" $o > /home/user/src/$r-shot.log 2>&1 )
  echo "$r: $(ls $o | wc -l) shots"
  rm -rf $d/sbuild/CMakeFiles
done
echo ALL DONE
