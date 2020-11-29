# Builds afl altered by our mod for external fuzzing as well as all of our
# targets.

NPROC = `nproc`
# 预下载数据所在目录
DATAPATH=/tmp

# AFL

AFL_VERSION=2.52b
AFL_MOD=afl-$(AFL_VERSION)-mod
AFL_DIR=$(AFL_MOD)/afl-$(AFL_VERSION)

ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

AFL_FUZZ=$(ROOT_DIR)/$(AFL_DIR)/afl-fuzz
AFL_GCC=$(ROOT_DIR)/$(AFL_DIR)/afl-gcc
AFL_GXX=$(ROOT_DIR)/$(AFL_DIR)/afl-g++
CFLAGS=-fsanitize=address
CXXFLAGS=-fsanitize=address

$(AFL_DIR):
	@echo " **** Downloading afl and applying fuzz1ng mod"
	cd $(AFL_MOD)/ && if [ ! -f afl-$(AFL_VERSION).tgz ]; then wget http://lcamtuf.coredump.cx/afl/releases/afl-$(AFL_VERSION).tgz; fi
	cd $(AFL_MOD)/ && tar xf afl-$(AFL_VERSION).tgz
	cp -R $(AFL_MOD)/mod/* $(AFL_DIR)/

$(AFL_DIR)/afl-fuzz: $(AFL_DIR)
	@echo " **** Building afl with fuzz1ng mod"
	cd $(AFL_DIR)/ && make -j$(NPROC)


# LAVA-M
LAVA_M_MOD = lava-m-mod
LAVA_M_DIR = $(LAVA_M_MOD)/lava_corpus
# LAVA_M_DIR = $(DATAPATH)/lava_corpus

# wget http://panda.moyix.net/~moyix/lava_corpus.tar.xz
# 注意LAVA-M需要手动安装acllib1
# sudo apt install libacl1 libacl1-dev
$(LAVA_M_DIR):
	@echo " **** Downloading lava-m"
	if [ ! -f $(DATAPATH)/lava_corpus.tar.xz ]; then wget http://panda.moyix.net/~moyix/lava_corpus.tar.xz -P $(DATAPATH); fi
	cd $(LAVA_M_MOD) && if [ ! -f lava_corpus.tar.xz ]; then cp $(DATAPATH)/lava_corpus.tar.xz ./; fi
	cd $(LAVA_M_MOD) && if [ ! -d lava_corpus ]; then tar xf lava_corpus.tar.xz; fi

$(LAVA_M_MOD)/base64_afl: $(LAVA_M_DIR)
	@echo " **** Building base64 with afl"
	cd $(LAVA_M_DIR)/LAVA-M/base64/coreutils-8.24-lava-safe && ./configure CC="$(AFL_GCC)" LIBS="-lacl"; make -j$(NPROC)
	cp $(LAVA_M_DIR)/LAVA-M/base64/coreutils-8.24-lava-safe/src/base64 $(LAVA_M_MOD)/base64_afl

$(LAVA_M_MOD)/md5sum_afl: $(LAVA_M_DIR)
	@echo " **** Building md5sum with afl"
	cd $(LAVA_M_DIR)/LAVA-M/md5sum/coreutils-8.24-lava-safe && ./configure CC="$(AFL_GCC)" LIBS="-lacl"; make -j$(NPROC)
	cp $(LAVA_M_DIR)/LAVA-M/md5sum/coreutils-8.24-lava-safe/src/md5sum $(LAVA_M_MOD)/md5sum_afl

$(LAVA_M_MOD)/uniq_afl: $(LAVA_M_DIR)
	@echo " **** Building uniq with afl"
	cd $(LAVA_M_DIR)/LAVA-M/uniq/coreutils-8.24-lava-safe && ./configure CC="$(AFL_GCC)" LIBS="-lacl"; make -j$(NPROC)
	cp $(LAVA_M_DIR)/LAVA-M/uniq/coreutils-8.24-lava-safe/src/uniq $(LAVA_M_MOD)/uniq_afl

$(LAVA_M_MOD)/who_afl: $(LAVA_M_DIR)
	@echo " **** Building who with afl"
	cd $(LAVA_M_DIR)/LAVA-M/who/coreutils-8.24-lava-safe && ./configure CC="$(AFL_GCC)" LIBS="-lacl"; make -j$(NPROC)
	cp $(LAVA_M_DIR)/LAVA-M/who/coreutils-8.24-lava-safe/src/who $(LAVA_M_MOD)/who_afl

all: $(AFL_DIR)/afl-fuzz $(LAVA_M_MOD)/base64_afl $(LAVA_M_MOD)/md5sum_afl $(LAVA_M_MOD)/uniq_afl $(LAVA_M_MOD)/who_afl \

clean:
	rm -rf $(AFL_DIR)
#	rm -rf $(AFL_MOD)/afl-$(AFL_VERSION).tgz
	rm -rf $(LAVA_M_MOD)/base64_afl
	rm -rf $(LAVA_M_MOD)/md5sum_afl
	rm -rf $(LAVA_M_MOD)/uniq_afl
	rm -rf $(LAVA_M_MOD)/who_afl
	rm -rf $(LAVA_M_DIR)
#	rm -rf $(LAVA_M_MOD)/lava_corpus.tar.xz
