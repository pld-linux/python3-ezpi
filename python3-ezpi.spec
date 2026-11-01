#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Simple library to read and write public-inbox
Summary(pl.UTF-8):	Prosta biblioteka do odczytu i zapisu repozytoriów public-inbox
Name:		python3-ezpi
Version:	0.7.0
Release:	1
License:	MIT-0
Group:		Libraries/Python
Source0:	https://www.kernel.org/pub/software/devel/ezpi/ezpi-%{version}.tar.xz
# Source0-md5:	e5e2a043107a9d5b69f128ddf8463402
URL:		https://pypi.org/project/ezpi/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools
BuildRequires:	python3-wheel
%if %{with tests}
BuildRequires:	git-core
BuildRequires:	python3-pygit2 >= 1.12
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme >= 2.0
BuildRequires:	sphinx-pdg-3 >= 7.0
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a small library for reading and writing public-inbox v2
repositories. Note, that this is not a suitable replacement for
public-inbox in itself - the goal is merely to provide a way to
produce and consume public-inbox repositories that can be cloned,
indexed and served from an actual public-inbox server running
elsewhere.

%description -l pl.UTF-8
Ten pakiet to prosta biblioteka do odczytu i zapisu repozytoriów
public-inbox v2. Nie jest to pełny zamiennik samego public-inbox -
celem jest głównie udostępnienie funkcjonalności produkcji i
konsumpcji repozytoriów public-inbox, które można klonować,
indeksować i udostępniać z właściwego serwera public-inbox,
działającego gdzieś indziej.

%package apidocs
Summary:	API documentation for Python ezpi module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona ezpi
Group:		Documentation

%description apidocs
API documentation for Python ezpi module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona ezpi.

%prep
%setup -q -n ezpi-%{version}

# 2 test case variants: 2099 fails with 32-bit time_t
%{__sed} -i -e '/future_date/ s/Jan 2099/Jan 2038/' tests/test_reading.py

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_bindir}/ezpi
%{py3_sitescriptdir}/ezpi
%{py3_sitescriptdir}/ezpi-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
