Name:           osmo-hnbgw
Version:        1.7.0
Release:        1.dcbw%{?dist}
Summary:        Osmocom Home NodeB Gateway, for attaching femtocells to the 3G CN
License:        AGPL-3.0-or-later

URL:            https://osmocom.org/projects/osmohnbgw/wiki

BuildRequires:  git gcc autoconf automake libtool doxygen systemd-devel
BuildRequires:  nftables-devel >= 1.0.2 lksctp-tools-devel
BuildRequires:  libosmocore-devel >= 1.10.0
BuildRequires:  libasn1c-devel >= 0.9.38
BuildRequires:  libosmo-netif-devel >= 1.6.0
BuildRequires:  libosmo-sigtran-devel >= 2.1.1
BuildRequires:  osmo-iuh-devel >= 1.7.0
BuildRequires:  libosmo-pfcp-devel >= 0.5.0
BuildRequires:  osmo-mgw-devel >= 1.14.0

Source0: %{name}-%{version}.tar.bz2

Requires: osmo-usergroup

%description
An Open Source implenentation of a HNB-GW (HomeNodeB-Gateway), implementing the
Iuh, IuCS and IuPS interfaces. It aggregates the Iuh links from femtocells
(hNodeBs) and presents them as regular IuCS and IuPS towards MSC and SGSN
(such as OsmoMSC and OsmoSGSN). It uses M3UA as signaling transport.


%prep
%autosetup -p1

%build
%global optflags %(echo %optflags | sed 's|-Wp,-D_GLIBCXX_ASSERTIONS||g')
echo "%{version}" >.tarball-version
autoreconf -fiv
%configure --enable-shared \
           --disable-static \
           --enable-nftables \
           --enable-pfcp \
           --with-systemdsystemunitdir=%{_unitdir}

# Fix unused direct shlib dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
# Remove libtool archives
find %{buildroot} -name '*.la' -exec rm -f {} \;


%check
make check


%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%post
%systemd_post %{name}.service

%files
%license COPYING
%doc README.md
%{_bindir}/osmo-hnbgw
%dir %{_docdir}/%{name}
%{_docdir}/%name/*
%{_unitdir}/%{name}.service
%attr(0644,root,root) %config(missingok,noreplace) %{_sysconfdir}/osmocom/%{name}.cfg

%changelog
* Sun Jun  8 2025 Dan Williams <dan@ioncontrol.co> - 1.7.0
- Update to 1.7.0

* Sun Aug 26 2018 Cristian Balint <cristian.balint@gmail.com>
- github update releases
