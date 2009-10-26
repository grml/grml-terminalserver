install_ = "install"

name = "grml-terminalserver"

etc = ${DESTDIR}/etc/grml/terminalserver
usr = ${DESTDIR}/usr
usrbin = $(usr)/bin
usrsbin = $(usr)/sbin
usrshare = $(usr)/share/$(name)

install:
	$(install_) -d -m 755 $(etc)
	$(install_) -m 644 config $(etc)

	$(install_) -d -m 755 $(usrshare)
	$(install_) -m 644 default_config $(usrshare)
	$(install_) -m 644 shared_prog_vars $(usrshare)
	$(install_) -m 755 nfs-kernel-server $(usrshare)
	$(install_) -m 644 terminalserver_netboot_package.conf $(usrshare)
	cp -r templates $(usrshare)

	$(install_) -m 755 -d $(usrsbin)
	$(install_) -m 755 grml-terminalserver $(usrsbin)
	$(install_) -m 755 grml-terminalserver-config $(usrsbin)
