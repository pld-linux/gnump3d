# TODO
# - use FHS (/var, /usr) instead of /home/services/gnump3d
Summary:	GNUMP3d is a streaming server for MP3s, OGG vorbis files, movies and other media formats
Summary(hu.UTF-8):	GNUMP3d egy stream server MP3, OGG, videó és egyéb média fájlokhoz.
Summary(pl.UTF-8):	GNUMP3d jest serwerem pozwalającym na strumieniowe transmisje dźwięku i filmów
Name:		gnump3d
Version:	3.0
Release:	0.1
License:	GPL v2+
Group:		Applications/Multimedia
Source0:	http://savannah.gnu.org/download/gnump3d/%{name}-%{version}.tar.bz2
# Source0-md5:	41786650bbc591484c08014a89478bf9
URL:		http://www.gnu.org/software/gnump3d/
BuildRequires:	sed >= 4.0
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(gnump3d)
Provides:	user(gnump3d)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNUMP3d is a streaming server for MP3s, OGG vorbis files, movies and
other media formats. It is designed to be:

- Small, stable, portable, self-contained, and secure.
- Simple to install, configure, and use.
- Portable across different varieties of Unix, the GNU Operating
  System, and Microsoft Windows platforms.

%description -l hu.UTF-8
GNUMP3d egy stream szerver MP3, OGG, videó és egyéb média fájlokhoz. A
következők jellemzik:

- kicsi, stabil, hordozható, biztonságos
- egyszerű telepítés, beállítás és használat
- hordozható a Unix különböző változatai, a GNU Operációs Rendszer és
  a Microsoft Windows platformok között

%description -l pl.UTF-8
GNUMP3d jest serwerem pozwalającym na strumieniowe transmisje danych
multimedialnych takich jak muzyka w formacie mp3 lub ogg oraz filmy.
HNUMP3d został tak zaprojektowany, aby być:

- mały, stabilny, przenośny, niezależny od innych programów,
  bezpieczny;
- łatwy do instalacji, skonfigurowania, uruchomienia;
- przenośny pomiędzy różnymi wersjami Uniksa, systemem GNU oraz
  systemami Microsoftu.

%prep
%setup -q
%{__sed} -i "s,\`perl.*\`,%{perl_vendorlib}/," Makefile

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	PREFIX=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}/man1

ln -sf gnump3d2 $RPM_BUILD_ROOT%{_bindir}/gnump3d
%{__sed} -i "s|^user =.*|user = gnump3d|" $RPM_BUILD_ROOT%{_sysconfdir}/gnump3d/gnump3d.conf
%{__sed} -i "s@/var/\([^/]*\)/gnump3d@/home/services/gnump3d/\1@" $RPM_BUILD_ROOT%{_sysconfdir}/gnump3d/gnump3d.conf
install -d $RPM_BUILD_ROOT/home/services/gnump3d/{log,cache}
touch $RPM_BUILD_ROOT/home/services/gnump3d/cache/serving

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 202 gnump3d
%useradd -u 202 -r -d /home/services/gnump3d -s /bin/false -c "GNUMP3d User" -g gnump3d gnump3d

%postun
if [ "$1" = "0" ]; then
	%userremove gnump3d
	%groupremove gnump3d
fi

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/gnump3d
# XXX %config tags for config files!
%{_sysconfdir}/gnump3d/*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*
%dir %{perl_vendorlib}/gnump3d
%{perl_vendorlib}/gnump3d/*

%dir /home/services/gnump3d
# XXX own dirs by root, let it be group writable, unless there's good reason otherwise
%attr(755,gnump3d,gnump3d) /home/services/gnump3d/log
%dir %attr(755,gnump3d,gnump3d) /home/services/gnump3d/cache
%attr(755,gnump3d,gnump3d) /home/services/gnump3d/cache/serving
