%include	/usr/lib/rpm/macros.python
%define		zope_subname	Silva
Summary:	A Zope-based web application
Summary(pl):	Aplikacja dla stron WWW oparta na Zope
Name:		Zope-%{zope_subname}
# %%define		sub_ver b1
Version:	0.9.3
Release:	2
License:	Distributable
Group:		Development/Tools
Source0:	http://zope.org/Members/infrae/%{zope_subname}/%{zope_subname}-%{version}/%{zope_subname}-%{version}-all.tgz
# Source0-md5:	a419a09c3980628d76ca6b87bc2d0cd8
URL:		http://zope.org/Members/infrae/Silva/
%pyrequires_eq	python-modules
Requires:	Zope >= 2.6.1
Requires:	Zope-Formulator
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
    docs/SilvaMetadata docs/SilvaViews docs/XMLWidgets
mv -f Annotations/{CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt} docs/Annotations
mv -f FileSystemSite/README.txt docs/FileSystemSite
mv -f ParsedXML/{CHANGES.txt,CREDITS.txt,INSTALL.txt,README.txt} docs/ParsedXML
mv -f ProxyIndex/{CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt} docs/ProxyIndex
mv -f Silva/{CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt,TROUBLESHOOTING.txt,UPGRADE.txt} docs/Silva
mv -f SilvaDocument/{DEVELOPER.txt,HISTORY.txt,INSTALL.txt,README.txt} docs/SilvaDocument
mv -f SilvaMetadata/{API.txt,CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt,ROADMAP.txt} docs/SilvaMetadata
mv -f SilvaViews/{CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt} docs/SilvaViews
mv -f XMLWidgets/{CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt} docs/XMLWidgets

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -af {Annotations,FileSystemSite,ParsedXML,ProxyIndex,Silva,SilvaDocument,SilvaMetadata,SilvaViews,XMLWidgets} \
    $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

# find $RPM_BUILD_ROOT -type f -name "*.py" -exec rm -rf {} \;;
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
for p in Annotations FileSystemSite ParsedXML ProxyIndex Silva SilvaDocument SilvaMetadata SilvaViews XMLWidgets ; do
    /usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%postun
if [ "$1" = "0" ]; then
    for p in Annotations FileSystemSite ParsedXML ProxyIndex Silva SilvaDocument SilvaMetadata SilvaViews XMLWidgets ; do
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
