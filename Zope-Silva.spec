%include	/usr/lib/rpm/macros.python
%define		zope_subname	Silva
Summary:	Silva - a Zope-based web application
Summary(pl):	Silva - aplikacja dla stron WWW oparta na Zope
Name:		Zope-%{zope_subname}
Version:	0.9.2.5
Release:	1
License:	Distributable
Group:		Development/Tools
Source0:	http://zope.org/Members/infrae/%{zope_subname}/%{zope_subname}-%{version}/%{zope_subname}-%{version}-all.tgz
# Source0-md5:	c8bf44d70e2ff98f2d45c47e179d8925
URL:		http://zope.org/Members/infrae/Silva/
%pyrequires_eq	python-modules
Requires:	python-PyXML >= 0.8.2
Requires:	Zope >= 2.6.1
Requires:	Zope-Formulator
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	product_dir	/usr/lib/zope/Products

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

mkdir docs docs/Annotations docs/FileSystemSite docs/ParsedXML docs/ProxyIndex docs/Silva docs/SilvaMetadata docs/XMLWidgets
mv -f Annotations/{CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt} docs/Annotations
mv -f FileSystemSite/README.txt docs/FileSystemSite
mv -f ParsedXML/{CHANGES.txt,CREDITS.txt,INSTALL.txt,README.txt} docs/ParsedXML
mv -f ProxyIndex/{CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt} docs/ProxyIndex
mv -f Silva/{CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt,TROUBLESHOOTING.txt,UPGRADE.txt} docs/Silva
mv -f SilvaMetadata/{API.txt,CREDITS.txt,INSTALL.txt,README.txt,ROADMAP.txt} docs/SilvaMetadata
mv -f XMLWidgets/{CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt} docs/XMLWidgets

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{product_dir}/%{zope_subname}

cp -af {Annotations,FileSystemSite,ParsedXML,ProxyIndex,Silva,SilvaMetadata,XMLWidgets} $RPM_BUILD_ROOT%{product_dir}

%py_comp $RPM_BUILD_ROOT%{product_dir}
%py_ocomp $RPM_BUILD_ROOT%{product_dir}

# find $RPM_BUILD_ROOT -type f -name "*.py" -exec rm -rf {} \;;
rm -rf $RPM_BUILD_ROOT%{product_dir}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%postun
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%{product_dir}/%{zope_subname}
%{product_dir}/Annotations
%{product_dir}/FileSystemSite
%{product_dir}/ParsedXML
%{product_dir}/ProxyIndex
%{product_dir}/SilvaMetadata
%{product_dir}/XMLWidgets
