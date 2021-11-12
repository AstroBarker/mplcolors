PREFIX = /usr
MANDIR = $(PREFIX)/share/man

all:
	@echo Run \'make install\' to install mplcolors.

install:
	@mkdir -p $(DESTDIR)$(PREFIX)/bin
	@mkdir -p $(DESTDIR)$(MANDIR)/man1
	@cp -p mplcolors.py $(DESTDIR)$(PREFIX)/bin/mplcolors
	@cp -p mplcolors.1 $(DESTDIR)$(MANDIR)/man1
	@chmod 755 $(DESTDIR)$(PREFIX)/bin/mplcolors

uninstall:
	@rm -rf $(DESTDIR)$(PREFIX)/bin/mplcolors
	@rm -rf $(DESTDIR)$(MANDIR)/man1/mplcolors.1*
