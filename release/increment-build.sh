#!/bin/sh
BUILD=`cat build`
BUILD=`expr $BUILD + 1`
echo $BUILD > build
echo Build now $BUILD
