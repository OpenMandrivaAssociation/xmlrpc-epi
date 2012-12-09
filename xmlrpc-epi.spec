%define major 0
%define libname %mklibname xmlrpc-epi %{major}
%define develname %mklibname xmlrpc-epi -d

Summary:	An implementation of the XML-RPC protocol in C
Name:		xmlrpc-epi
Version:	0.54.2
Release:	1
License:	BSD
Group:		System/Libraries
URL:		http://xmlrpc-epi.sourceforge.net
Source0:	http://sunet.dl.sourceforge.net/sourceforge/xmlrpc-epi/xmlrpc-epi-%{version}.tar.bz2
Patch0:		xmlrpc-epi-0.51-format_not_a_string_literal_and_no_format_arguments.diff
Patch1:		xmlrpc-epi-0.54-no_samples.diff
BuildRequires:	expat-devel

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
Requires:	%{libname} >= %{version}-%{release}
Provides:	libxmlrpc-devel = %{version}-%{release}
Provides:	xmlrpc-epi-devel = %{version}-%{release}

%description -n	%{develname}
xmlrpc-epi is an implementation of the xmlrpc protocol in C. It provides an
easy to use API for developers to serialize RPC requests to and from XML.
It does *not* include a transport layer, such as HTTP. The API is primarily
based upon proprietary code written for internal usage at Epinions.com, and
was later modified to incorporate concepts from the xmlrpc protocol.

%prep

%setup -q
%patch0 -p1 -b .format_not_a_string_literal_and_no_format_arguments
%patch1 -p0 -b .no_samples

# Make it lib64 aware
find . -name "Makefile.*" | xargs perl -pi -e "s,-L\@prefix\@/lib,,g"

perl -pi -e "s,-L/usr/local/lib\b,," configure*
perl -pi -e "s|withval/lib|withval/%{_lib}|g" configure*

%build
autoreconf -fi

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

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

%files -n %{libname}
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%doc INSTALL
%dir %{_includedir}/xmlrpc-epi
%{_includedir}/xmlrpc-epi/*
%{_libdir}/lib*.so


%changelog
* Sun Jan 29 2012 Oden Eriksson <oeriksson@mandriva.com> 0.54.2-1
+ Revision: 769633
- 0.54.2

* Thu Dec 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.54.1-3
+ Revision: 739018
- drop the static lib and the libtool *.la file
- various fixes

* Sat May 07 2011 Oden Eriksson <oeriksson@mandriva.com> 0.54.1-2
+ Revision: 671350
- mass rebuild

* Mon Aug 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.54.1-1mdv2011.0
+ Revision: 568118
- 0.54.1

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 0.54-3mdv2010.1
+ Revision: 519082
- rebuild

* Fri Jun 12 2009 Oden Eriksson <oeriksson@mandriva.com> 0.54-2mdv2010.0
+ Revision: 385409
- use the correct libname
- don't build the samples
- move the header files to the correct place
- cleanup the spec file some

* Wed Jun 10 2009 Oden Eriksson <oeriksson@mandriva.com> 0.54-1mdv2010.0
+ Revision: 384837
- 0.54
- nuke redundant patches
- rediffed the format string patch

* Thu Dec 25 2008 Oden Eriksson <oeriksson@mandriva.com> 0.51-16mdv2009.1
+ Revision: 319111
- fix build with -Werror=format-security (P3)

* Thu Jun 19 2008 Thierry Vignaud <tv@mandriva.org> 0.51-15mdv2009.0
+ Revision: 226067
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.51-14mdv2008.1
+ Revision: 179490
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 0.51-13mdv2008.0
+ Revision: 39325
- fix provides (thanks blino!)

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 0.51-12mdv2008.0
+ Revision: 39288
- rebuild

* Wed Jun 13 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.51-11mdv2008.0
+ Revision: 38418
- fix building (spturtle :)
- use hack for parallel build
- drop br on automake1.4
- fix mixture of tabs and spaces
- spec file clean

* Mon Apr 23 2007 Frederic Crozat <fcrozat@mandriva.com> 0.51-10mdv2008.0
+ Revision: 17465
- Fix buildrequires
- Patch2 (Linden Labs): link to system expat lib, don't use internal copy


* Tue Oct 31 2006 Oden Eriksson <oeriksson@mandriva.com> 0.51-9mdv2007.0
+ Revision: 74648
- bunzip patches
- Import xmlrpc-epi

* Tue May 23 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.51-8mdk
- rebuild

* Wed Aug 10 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.51-7mdk
- gcc4 & mklibname fixes
- drop provides libxmlrpc

* Sat Aug 14 2004 Pixel <pixel@mandrakesoft.com> 0.51-6mdk
- rebuild

