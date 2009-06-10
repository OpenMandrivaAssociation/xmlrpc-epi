%define major 0
%define libname_orig xmlrpc
%define libname %mklibname %{libname_orig} %{major}

Summary:	An implementation of the XML-RPC protocol in C
Name:		xmlrpc-epi
Version:	0.54
Release:	%mkrel 1
License:	BSD
Group:		System/Libraries
URL:		http://xmlrpc-epi.sourceforge.net
Source0:	http://sunet.dl.sourceforge.net/sourceforge/xmlrpc-epi/xmlrpc-epi-%{version}.tar.gz
Patch0:		xmlrpc-epi-0.51-format_not_a_string_literal_and_no_format_arguments.diff
BuildRequires:	expat-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
xmlrpc-epi is an implementation of the xmlrpc protocol in C. It provides an 
easy to use API for developers to serialize RPC requests to and from XML.
It does *not* include a transport layer, such as HTTP. The API is primarily
based upon proprietary code written for internal usage at Epinions.com, and
was later modified to incorporate concepts from the xmlrpc protocol.

%package -n %{libname} 
Summary:	Library providing XMLPC support in C
Group:		System/Libraries
%if "%{_lib}" != "lib"
Conflicts:	libxmlrpc0 < 0.51-7mdk
%endif

%description -n %{libname}
xmlrpc-epi is an implementation of the xmlrpc protocol in C. It provides an 
easy to use API for developers to serialize RPC requests to and from XML.
It does *not* include a transport layer, such as HTTP. The API is primarily
based upon proprietary code written for internal usage at Epinions.com, and
was later modified to incorporate concepts from the xmlrpc protocol.
 
%package -n %{libname}-devel
Summary:	Libraries, includes, etc. to develop XML and HTML applications
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{libname_orig}-devel = %{version}-%{release}
%if "%{_lib}" != "lib"
Conflicts:	libxmlrpc0-devel < 0.51-7mdk
%endif

%description -n %{libname}-devel
xmlrpc-epi is an implementation of the xmlrpc protocol in C. It provides an
easy to use API for developers to serialize RPC requests to and from XML.
It does *not* include a transport layer, such as HTTP. The API is primarily
based upon proprietary code written for internal usage at Epinions.com, and
was later modified to incorporate concepts from the xmlrpc protocol.

%prep

%setup -q
%patch0 -p1 -b .format_not_a_string_literal_and_no_format_arguments

# Make it lib64 aware
find . -name "Makefile.*" | xargs perl -pi -e "s,-L\@prefix\@/lib,,g"

perl -pi -e "s,-L/usr/local/lib\b,," configure*
perl -pi -e "s|withval/lib|withval/%{_lib}|g" configure*

%build
autoreconf -fis

%configure2_5x \
    --with-expat=%{_prefix}

#don't use parallel compilation, it is broken 
# (tpg) this is better ;)
%(echo %make|perl -pe 's/-j\d+/-j1/g')

%install
rm -rf %{buildroot}

%makeinstall_std

# remove unpackaged files
rm -f %{buildroot}%{_bindir}/{client,hello_{client,server},memtest,sample,server{,_compliance_test}}

%clean
rm -rf %{buildroot}


%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/lib*.so.%{major}*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc INSTALL
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/lib*.a
