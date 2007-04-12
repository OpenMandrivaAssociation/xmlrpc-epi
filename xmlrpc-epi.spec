%define name		xmlrpc-epi
%define version		0.51
%define release		%mkrel 9

%define lib_major	0
%define lib_name_orig	xmlrpc
%define lib_name	%mklibname %{lib_name_orig} %{lib_major}

Summary:	An implementation of the XML-RPC protocol in C
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group: 		System/Libraries
BuildRoot:	%_tmppath/%name-%version-%release-root
URL:		http://xmlrpc-epi.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		xmlrpc-epi-0.51-64bit-fixes.patch
Patch1:		xmlrpc-epi-0.51-gcc4.patch

%description
xmlrpc-epi is an implementation of the xmlrpc protocol in C. It provides an 
easy to use API for developers to serialize RPC requests to and from XML.
It does *not* include a transport layer, such as HTTP. The API is primarily
based upon proprietary code written for internal usage at Epinions.com, and
was later modified to incorporate concepts from the xmlrpc protocol.

%package -n %{lib_name} 
Summary:	Library providing XMLPC support in C
Group: 		System/Libraries
%if "%{_lib}" != "lib"
Conflicts:	libxmlrpc0 < 0.51-7mdk
%endif

%description -n %{lib_name}
xmlrpc-epi is an implementation of the xmlrpc protocol in C. It provides an 
easy to use API for developers to serialize RPC requests to and from XML.
It does *not* include a transport layer, such as HTTP. The API is primarily
based upon proprietary code written for internal usage at Epinions.com, and
was later modified to incorporate concepts from the xmlrpc protocol.
 
%package -n %{lib_name}-devel
Summary: Libraries, includes, etc. to develop XML and HTML applications
Group: Development/C
Requires: %{lib_name} = %{version}
Provides: lib%{lib_name_orig}-devel = %{version}
%if "%{_lib}" != "lib"
Conflicts: libxmlrpc0-devel < 0.51-7mdk
%endif

%description -n %{lib_name}-devel
xmlrpc-epi is an implementation of the xmlrpc protocol in C. It provides an
easy to use API for developers to serialize RPC requests to and from XML.
It does *not* include a transport layer, such as HTTP. The API is primarily
based upon proprietary code written for internal usage at Epinions.com, and
was later modified to incorporate concepts from the xmlrpc protocol.

%prep
%setup -q
%patch0 -p1 -b .64bit-fixes
%patch1 -p1 -b .gcc4

# Make it lib64 aware
find . -name Makefile.in | xargs perl -pi -e "s,-L\@prefix\@/lib,,g"
perl -pi -e "s,-L/usr/local/lib\b,," configure

%build
%configure2_5x

#cp %{_datadir}/automake-1.6/depcomp .

#don't use parallel compilation, it is broken 
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_bindir}/{client,hello_{client,server},memtest,sample,server{,_compliance_test}}

%clean
rm -rf $RPM_BUILD_ROOT


%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files -n %{lib_name}
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/lib*.so.*

%files -n %{lib_name}-devel
%defattr(-, root, root)
%doc INSTALL
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/lib*.a


