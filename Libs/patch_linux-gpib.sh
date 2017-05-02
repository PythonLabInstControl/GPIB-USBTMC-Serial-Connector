# this script patches the supplied linux-gpib sources
# with support for the gpio-driven RasPi-GPIB driver
tar xzf linux-gpib-*.tar.gz
cd linux-gpib*
./configure
cd ..
patch -p0 < RasPi_GPIB_driver.patch
cd linux-gpib*
make
