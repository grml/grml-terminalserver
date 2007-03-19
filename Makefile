install_ = "install"

name = "grml-terminalserver"

#ifndef CFLAGS
CFLAGS = -Wall -O2
#endif

etc = ${DESTDIR}/etc/grml/terminalserver
usr = ${DESTDIR}/usr
usrbin = $(usr)/bin
usrsbin = $(usr)/sbin
usrshare = $(usr)/share/$(name)

bin: timeout

timeout: timeout.c
	diet gcc $(CFLAGS) $^ -o $@
	strip --strip-unneeded $@

install: bin
	$(install_) -d -m 755 $(etc)
	$(install_) -m 644 config $(etc)

	$(install_) -d -m 755 $(usrshare)
	$(install_) -m 644 grub_cards $(usrshare)
	$(install_) -m 644 default_config $(usrshare)
	$(install_) -m 644 shared_prog_vars $(usrshare)
	$(install_) -m 755 nfs-kernel-server $(usrshare)
	$(install_) -m 644 terminalserver_netboot_package.conf $(usrshare)
	$(install_) -m 755 linuxrc $(usrshare)
	$(install_) -m 755 udhcp-config.sh $(usrshare)
	$(install_) -m 755 rdir $(usrshare)
	$(install_) -m 755 cdir $(usrshare)
	$(install_) -m 755 timeout $(usrshare)
	cp -r templates $(usrshare)

	$(install_) -m 755 -d $(usrsbin)
	$(install_) -m 755 grml-terminalserver $(usrsbin)
	$(install_) -m 755 grml-terminalserver-config $(usrsbin)

clean:
	rm -f timeout
