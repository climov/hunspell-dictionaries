Name: hunspell-ur
Summary: Urdu hunspell dictionaries
Version: 0.64
Release: 2.1%{?dist}
#http://urdudictionary.codeplex.com/Release/ProjectReleases.aspx?ReleaseId=30004#DownloadId=74761
#and click yes to agree to LGPLv2+, which stinks as a download-url :-(
Source: UrduDictionary.xpi
Group: Applications/Text
URL: http://urdudictionary.codeplex.com
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
License: LGPLv2+
BuildArch: noarch
BuildRequires: redland

Requires: hunspell

%description
Urdu hunspell dictionaries.

%prep
%setup -q -c -n hunspell-ur

%build
rdfproc hunspell-ur parse install.rdf
rdfproc hunspell-ur print | grep install-manifest | grep -v targetApplication | sed -e 's/.*#//' | sed -e 's/], "/: /'| sed -e 's/"}//' > CREDITS

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p dictionaries/ur.aff $RPM_BUILD_ROOT/%{_datadir}/myspell/ur_PK.aff
cp -p dictionaries/ur.dic $RPM_BUILD_ROOT/%{_datadir}/myspell/ur_PK.dic
pushd $RPM_BUILD_ROOT/%{_datadir}/myspell/
ur_PK_aliases="ur_IN"
for lang in $ur_PK_aliases; do
        ln -s ur_PK.aff $lang.aff
        ln -s ur_PK.dic $lang.dic
done
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CREDITS
%{_datadir}/myspell/*

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.64-2.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.64-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 09 2009 Caolan McNamara <caolanm@redhat.com> - 0.64-1
- latest version

* Thu Apr 30 2009 Caolan McNamara <caolanm@redhat.com> - 0.61-1
- latest version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 17 2006 Caolan McNamara <caolanm@redhat.com> - 0.6-1
- initial version
