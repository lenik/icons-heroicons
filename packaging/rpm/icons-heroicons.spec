# Version is injected by packaging/rpm/Makefile via `zfr version`.
# RPM Version cannot contain '-'; use `zfr version -r` (hyphens → '_').
# srcversion is the unsanitized Meson/git version and names the tarball.
%{!?version:%global version 0.0.0}
%{!?srcversion:%global srcversion %{version}}

Name:           icons-heroicons
Version:        %{version}
Release:        1%{?dist}
Summary:        Heroicons SVG icon set from Tailwind Labs

License:        AGPL-3.0-or-later
URL:            https://heroicons.com/
Packager:       Lenik (谢继雷) <lenik@bodz.net>
Source0:        %{name}-%{srcversion}.tar.xz

%global debug_package %{nil}
BuildArch:      noarch
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  python3
BuildRequires:  iconlibutils
BuildRequires:  asciidoctor
Requires:       iconlibutils

%description
Heroicons SVG icon set from Tailwind Labs
.
Provides icon assets under /usr/share/icons-heroicons, a preview index, and a
launcher `icons-heroicons` (`iconlib -l heroicons`).

%prep
%setup -q -n %{name}-%{srcversion}

%build
meson setup build \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --datadir=%{_datadir} \
    --mandir=%{_mandir} \
    --sysconfdir=%{_sysconfdir} \
    --localstatedir=%{_localstatedir} \
    --buildtype=plain
meson compile -C build

%install
meson install -C build --destdir=%{buildroot}

%files
%{_bindir}/icons-heroicons
%{_datadir}/bash-completion/completions/icons-heroicons
%{_datadir}/icons-heroicons/
%{_datadir}/doc/icons-heroicons/

%changelog
* Thu Aug 20 2026 Lenik (谢继雷) <lenik@bodz.net>
- Align spec with debian/control (Meson, AGPL-3.0-or-later).
- Version comes from `zfr version`, the same method meson.build uses.
