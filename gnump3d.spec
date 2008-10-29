Summary:	GNUMP3d is a streaming server for MP3s, OGG vorbis files, movies and other media formats
Summary(hu.UTF-8):	GNUMP3d egy stream server MP3, OGG, videó és egyéb média fájlokhoz.
Name:		gnump3d
Version:	3.0
Release:	0.1
License:	GPL v2+
Group:		Applications/Multimedia
Source0:	http://savannah.gnu.org/download/gnump3d/%{name}-%{version}.tar.bz2
# Source0-md5:	41786650bbc591484c08014a89478bf9
URL:		http://www.gnu.org/software/gnump3d/
BuildRequires:	perl-Config-File
BuildRequires:	sed > 4.0
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
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

%prep
%setup -q
%{__sed} -i "s,\`perl.*\`,%{perl_vendorlib}/," Makefile

%build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}/man1
cd $RPM_BUILD_ROOT%{_bindir}
ln -sf gnump3d{2,}
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
%userremove gnump3d
%groupremove gnump3d


%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*

%dir %{perl_vendorlib}/gnump3d
%{perl_vendorlib}/gnump3d/*

%dir %{_sysconfdir}/gnump3d
%{_sysconfdir}/gnump3d/*

%dir /home/services/gnump3d
%attr(755,gnump3d,gnump3d) /home/services/gnump3d/log
%attr(755,gnump3d,gnump3d) /home/services/gnump3d/cache
%attr(755,gnump3d,gnump3d) /home/services/gnump3d/cache/serving
