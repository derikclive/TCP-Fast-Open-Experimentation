sudo apt-get -y install autoconf autogen automake libtool gtk-doc-tools xsltproc\
 gettext zlib1g-dev liblzma-dev libbz2-dev libgnutls-dev libidn2-0-dev flex \
libssl-dev

cd ~; git clone http://github.com/rockdaboot/mget

cd mget

./autogen.sh

./configure

make

sudo make install

touch ~/.mgetrc
