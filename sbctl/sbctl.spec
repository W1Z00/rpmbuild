# Modified from https://github.com/chenxiaolong/fedora-packages/blob/master/copr/sbctl/sbctl/sbctl.spec
Name:           sbctl
Version:        0.18
Release:        1%{?dist}
License:        MIT
Summary:        Secure Boot Key Manager
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-%{version}.tar.gz.sig
Source2:        https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xc100346676634e80c940fb9e9c02ff419fecbe16

ExclusiveArch:  %{golang_arches}

Requires:       binutils
Requires:       util-linux

Recommends:     systemd-udev

BuildRequires:  golang >= 1.20
BuildRequires:  asciidoc
BuildRequires:  go-rpm-macros
BuildRequires:  pkgconfig(libpcsclite)
BuildRequires:  gpgverify

%description
Self-compiled binary

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

sed -i.orig '/go build/d' Makefile
! diff -q Makefile.orig Makefile

sed -i.orig '/libpcsclite_real\.so\.1/ s,/usr/lib,%{_libdir},' lsm/lsm.go
! diff -q lsm/lsm.go.orig lsm/lsm.go

%build
%global gomodulesmode GO111MODULE=on
%gobuild -o sbctl ./cmd/sbctl
%make_build

%install
%make_install PREFIX=%{_prefix}

# Unused
rm %{buildroot}%{_prefix}/lib/kernel/postinst.d/91-sbctl.install

%files
%license LICENSE
%doc README.md
%ghost %dir %{_sysconfdir}/sbctl
%ghost %config(noreplace) %{_sysconfdir}/sbctl/sbctl.conf
%{_bindir}/sbctl
%{_prefix}/lib/kernel/install.d/91-sbctl.install
%{_mandir}/man5/sbctl.conf.5*
%{_mandir}/man8/sbctl.8*
%{bash_completions_dir}/sbctl
%{fish_completions_dir}/sbctl.fish
%{zsh_completions_dir}/_sbctl
