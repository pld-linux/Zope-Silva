%include	/usr/lib/rpm/macros.python
%define		zope_subname	Silva
Summary:	A Zope-based web application
Summary(pl):	Aplikacja dla stron WWW oparta na Zope
Name:		Zope-%{zope_subname}
%define		sub_ver b1
Version:	1.0
Release:	0.%{sub_ver}.1
License:	Distributable
Group:		Development/Tools
Source0:	http://zope.org/Members/infrae/%{zope_subname}/%{zope_subname}-%{version}%{sub_ver}/%{zope_subname}-%{version}%{sub_ver}-all.tgz
# Source0-md5:	491da24183aa129a5397afbda6765452
URL:		http://zope.org/Members/infrae/Silva/
%pyrequires_eq	python-modules
Requires:	Zope >= 2.6.1
Requires:	Zope-Formulator >= 1.6.2
Requires:	Zope-FileSystemSite
Requires:	python-PyXML >= 0.8.3
Requires(post,postun):  /usr/sbin/installzopeproduct
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Silva is a Zope-based web application designed for the creation and
management of structured, textual content.

%description -l pl
Silva to aplikacja dla stron WWW oparta na Zope, zaprojektowana do
tworzenia i zarz±dzania struktur± tre¶ci tekstowej.

%prep
%setup -q -c

%build
# remove dirs - additional packages!
rm -rf Formulator

mkdir docs docs/Annotations docs/FileSystemSite docs/ParsedXML docs/ProxyIndex docs/Silva docs/SilvaDocument \
    docs/SilvaMetadata docs/SilvaViews docs/XMLWidgets docs/kupu
mv -f Annotations/{CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt} docs/Annotations
mv -f FileSystemSite/README.txt docs/FileSystemSite
mv -f ParsedXML/{CHANGES.txt,CREDITS.txt,INSTALL.txt,README.txt} docs/ParsedXML
mv -f ProxyIndex/{CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt} docs/ProxyIndex
mv -f Silva/{CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt,TROUBLESHOOTING.txt,UPGRADE.txt} docs/Silva
mv -f SilvaDocument/{DEVELOPER.txt,HISTORY.txt,INSTALL.txt,README.txt} docs/SilvaDocument
mv -f SilvaMetadata/{API.txt,CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt,ROADMAP.txt} docs/SilvaMetadata
mv -f SilvaViews/{CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt} docs/SilvaViews
mv -f XMLWidgets/{CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt} docs/XMLWidgets
mv -f kupu/doc/* docs/kupu
mv -f kupu/README*.txt docs/kupu
rm -rf kupu/doc
rm -rf kupu/{Makefile,make.bat}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -af {Annotations,FileSystemSite,ParsedXML,ProxyIndex,Silva,SilvaDocument,SilvaMetadata,SilvaViews,XMLWidgets,kupu} \
    $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

# find $RPM_BUILD_ROOT -type f -name "*.py" -exec rm -rf {} \;;
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
for p in Annotations FileSystemSite ParsedXML ProxyIndex Silva SilvaDocument SilvaMetadata SilvaViews XMLWidgets kupu; do
    /usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%postun
if [ "$1" = "0" ]; then
    for p in Annotations FileSystemSite ParsedXML ProxyIndex Silva SilvaDocument SilvaMetadata SilvaViews XMLWidgets kupu; do
        /usr/sbin/installzopeproduct -d $p
    done
fi
if [ -f /var/lock/subsys/zope ]; then
            /etc/rc.d/init.d/zope restart >&2
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%{_datadir}/%{name}
