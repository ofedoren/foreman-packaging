# template: scl
%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name sidekiq

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 5.2.7
Release: 1%{?dist}
Summary: Simple, efficient background processing for Ruby
Group: Development/Languages
License: LGPL-3.0
URL: http://sidekiq.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

# start specfile generated dependencies
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby >= 2.2.2
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(redis) >= 3.3.5
Requires: %{?scl_prefix}rubygem(redis) < 5
Requires: %{?scl_prefix}rubygem(connection_pool) >= 2.2
Requires: %{?scl_prefix}rubygem(connection_pool) < 3
Requires: %{?scl_prefix}rubygem(connection_pool) >= 2.2.2
Requires: %{?scl_prefix_ruby}rubygem(rack) >= 1.5.0
Requires: %{?scl_prefix_ror}rubygem(rack-protection) >= 1.5.0
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}ruby >= 2.2.2
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
# end specfile generated dependencies

%description
Simple, efficient background processing for Ruby.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%{?scl:EOF}

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/
find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%files
%dir %{gem_instdir}
%{_bindir}/sidekiq
%{_bindir}/sidekiqctl
%{gem_instdir}/.circleci
%{gem_instdir}/.github
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%{gem_instdir}/3.0-Upgrade.md
%{gem_instdir}/4.0-Upgrade.md
%{gem_instdir}/5.0-Upgrade.md
%license %{gem_instdir}/COMM-LICENSE
%{gem_instdir}/Changes.md
%{gem_instdir}/Ent-Changes.md
%license %{gem_instdir}/LICENSE
%{gem_instdir}/Pro-2.0-Upgrade.md
%{gem_instdir}/Pro-3.0-Upgrade.md
%{gem_instdir}/Pro-4.0-Upgrade.md
%{gem_instdir}/Pro-Changes.md
%{gem_instdir}/bin
%{gem_instdir}/code_of_conduct.md
%{gem_libdir}
%{gem_instdir}/web
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/sidekiq.gemspec

%changelog
