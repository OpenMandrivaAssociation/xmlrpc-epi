%define major 0
%define libname %mklibname xmlrpc-epi %{major}
%define develname %mklibname xmlrpc-epi -d

Summary:	An implementation of the XML-RPC protocol in C
Name:		xmlrpc-epi
Version:	0.54.1
Release:	%mkrel 2
License:	BSD
Group:		System/Libraries
URL:		http://xmlrpc-epi.sourceforge.net
Source0:	http://sunet.dl.sourceforge.net/sourceforge/xmlrpc-epi/xmlrpc-epi-%{version}.tar.gz
Patch0:		xmlrpc-epi-0.51-format_not_a_string_literal_and_no_format_arguments.diff
Patch1:		xmlrpc-epi-0.54-no_samples.diff
BuildRequires:	expat-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
xmlrpc-epi is an implementation of the xmlrpc protocol in C. It provides an 
easy to use API for developers to serialize RPC requests to and from XML.
It does *not* include a transport layer, such as HTTP. The API is primarily
based upon proprietary code written for internal usage at Epinions.com, and
was later modified to incorporate concepts from the xmlrpc protocol.

%package -n	%{libname} 
Summary:	Library providing XMLPC support in C
Group:		System/Libraries

%description -n	%{libname}
xmlrpc-epi is an implementation of the xmlrpc protocol in C. It provides an 
easy to use API for developers to serialize RPC requests to and from XML.
It does *not* include a transport layer, such as HTTP. The API is primarily
based upon proprietary code written for internal usage at Epinions.com, and
was later modified to incorporate concepts from the xmlrpc protocol.
 
%package -n	%{develname}
Summary:	Libraries, includes, etc. to develop XML and HTML applications
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	libxmlrpc-devel = %{version}-%{release}
Provides:	xmlrpc-epi-devel = %{version}-%{release}

%description -n	%{develname}
xmlrpc-epi is an implementation of the xmlrpc protocol in C. It provides an
easy to use API for developers to serialize RPC requests to and from XML.
It does *not* include a transport layer, such as HTTP. The API is primarily
based upon proprietary code written for internal usage at Epinions.com, and
was later modified to incorporate concepts from the xmlrpc protocol.

%prep

%setup -q -n xmlrpc
%patch0 -p1 -b .format_not_a_string_literal_and_no_format_arguments
%patch1 -p0 -b .no_samples

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

# fix file conflicts
install -d %{buildroot}%{_includedir}/xmlrpc-epi
mv %{buildroot}%{_includedir}/*.h %{buildroot}%{_includedir}/xmlrpc-epi/

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc INSTALL
%dir %{_includedir}/xmlrpc-epi
%{_includedir}/xmlrpc-epi/*
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/lib*.a
