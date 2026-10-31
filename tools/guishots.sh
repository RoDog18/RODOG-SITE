#!/bin/bash
# For plugins without a Shot tool: build the test runner and keep the GUI snapshots it writes (gui-*.png).
for r in "$@"; do
  d=/home/user/src/$r; o=/home/user/shots/$r; t=/home/user/src/$r-tests; mkdir -p $o $t
  [ -d $d/.git ] || git clone -q --depth 1 https://github.com/RoDog18/$r $d || { echo "$r: clone failed"; continue; }
  grep -q PLUGIN_TESTS $d/CMakeLists.txt || { echo "$r: no test runner"; continue; }
  ( cd $d && cmake -B tbuild -G Ninja -DCMAKE_BUILD_TYPE=Release -DJUCE_DIR=/home/user/JUCE -DPLUGIN_FORMATS=VST3 -DPLUGIN_TESTS=ON > /home/user/src/$r-tcfg.log 2>&1 \
    && cmake --build tbuild --target PluginTests -j4 > /home/user/src/$r-tbuild.log 2>&1 ) || { echo "$r: build failed"; continue; }
  bin=$(find $d/tbuild -type f -name PluginTests -perm -u+x | head -1)
  mkdir -p /home/user/src/home-$r
  ( cd $t && HOME=/home/user/src/home-$r timeout 900 "$bin" $t > /home/user/src/$r-tests.log 2>&1 )
  find $t -name 'gui-*.png' -exec cp {} $o/ \;
  echo "$r: $(ls $o | wc -l) shots"
  rm -rf $d/tbuild/CMakeFiles
done
echo GUI DONE
