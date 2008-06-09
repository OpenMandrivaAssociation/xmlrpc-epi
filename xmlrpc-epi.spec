%define major 0
%define libname_orig xmlrpc
%define libname %mklibname %{libname_orig} %{major}

Summary:	An implementation of the XML-RPC protocol in C
Name:		xmlrpc-epi
Version:	0.51
Release:	%mkrel 14
License:	BSD
Group:		System/Libraries
URL:		http://xmlrpc-epi.sourceforge.net
Source0:	%{name}-%{version}.tar.bz2
Patch0:		xmlrpc-epi-0.51-64bit-fixes.patch
Patch1:		xmlrpc-epi-0.51-gcc4.patch
# (fc) 0.51-10mdv build using system expat (Linden Labs)
Patch2:		xmlrpc-epi-0.51-excise_expat.patch
BuildRequires:	expat-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
%patch0 -p1 -b .64bit-fixes
%patch1 -p1 -b .gcc4
%patch2 -p1 -b .excice_expat

#needed by patch2
libtoolize --copy --force
aclocal
autoconf
automake -a -c --foreign

# Make it lib64 aware
find . -name Makefile.in | xargs perl -pi -e "s,-L\@prefix\@/lib,,g"
perl -pi -e "s,-L/usr/local/lib\b,," configure

%build
%configure2_5x


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
