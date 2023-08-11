%define shver 3
%define libname %mklibname svm
%define devname %mklibname svm -d
%define oldlibname %mklibname svm 2

%global libdir_libsvm %{_libdir}/libsvm
%global python3_libsvm_dir %{python3_sitearch}/libsvm
%global maven_group_id tw.edu.ntu.csie
%global pom_file_version 3.25
%global pom_file_name JPP.%{maven_group_id}-%{name}.pom
%global octpkg %{name}
%global release_date 2023-02-28
%global cpp_std c++17

%{!?_javadir: %global _javadir %{_datadir}/java}
%{!?_javadocdir: %global _javadocdir %{_datadir}/javadoc}

%{!?pyver: %define pyver %(python -c 'import sys; print(sys.version[0:3])')}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define libsvm_python_dir %{python_sitearch}/libsvm

%define javac javac
%define jar jar
%define libdir_libsvm %{_libdir}/libsvm
%define moc_path %{qt5dir}/bin/moc

%bcond_without java
%bcond_with maven
%bcond_without octave
%bcond_without python
%bcond_with gtk
%bcond_without qt

Summary:	A Library for Support Vector Machines
Name:		libsvm
Version:	3.32
Release:	1
License:	BSD
URL:		https://www.csie.ntu.edu.tw/~cjlin/libsvm/
Source0:	https://www.csie.ntu.edu.tw/~cjlin/libsvm/%{name}-%{version}.tar.gz
Source1:	https://www.csie.ntu.edu.tw/~cjlin/libsvm/log
Source2:	https://www.csie.ntu.edu.tw/~cjlin/papers/guide/guide.pdf
Source3:	libsvm-svm-toy-gtk.desktop
Source4:	libsvm-svm-toy-qt.desktop
Source5:	LibSVM-svm-toy-48.png
# Java interface files
Source6:	https://repo1.maven.org/maven2/tw/edu/ntu/csie/%{name}/%{pom_file_version}/%{name}-%{pom_file_version}.pom
Source7:	libsvm.INDEX
Source8:	libsvm.CITATION
Source9:	libsvm.DESCRIPTION
Source10:	%{name}.rpmlintrc

Patch0:	 %{name}-3.31.packageMain.patch
Patch1:	 %{name}-3.31.pythonDir.patch
Patch2:	 %{name}-3.31.javaDir.patch
Patch3:	 %{name}-3.31.svm-toy.patch
Patch4:	 %{name}-3.31.toolsDir.patch

%description
LIBSVM is an integrated software for support vector classification,
(C-SVC, nu-SVC ), regression (epsilon-SVR, nu-SVR) and distribution
estimation (one-class SVM ). It supports multi-class classification.

#---------------------------------------------------------------------------

%package -n svm-tools
Summary:	A Library for Support Vector Machines

%description -n svm-tools
LIBSVM is an integrated software for support vector classification,
(C-SVC, nu-SVC ), regression (epsilon-SVR, nu-SVR) and distribution
estimation (one-class SVM). It supports multi-class classification.

This packages provides some siplme tools.

%files -n svm-tools
%doc COPYRIGHT FAQ.html ChangeLog guide.pdf
%{_bindir}/svm-predict
%{_bindir}/svm-scale
%{_bindir}/svm-train
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/examples

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:		Header file, object file, and source files of libsvm in C, C++ and Java
BuildRequires:	glibc-devel 
BuildRequires:	gawk
Requires: 		svm-tools = %{version}-%{release}

%description -n %{libname}
LIBSVM is an integrated software for support vector classification,
(C-SVC, nu-SVC ), regression (epsilon-SVR, nu-SVR) and distribution
estimation (one-class SVM ). It supports multi-class classification.

This package provdes the libsvm shared library.

%files -n %{libname}
%{_libdir}/%{name}.so.%{shver}

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	Header file, object file, and source files of libsvm in C, C++ and Java
BuildRequires:	glibc-devel gawk
Requires: 	svm-tools = %{version}-%{release}
Provides:	%{name}-devel

%description -n %{devname}
Header file, object file of libsvm in C, C++ and Java.
Install this package if you want to develop programs with libsvm.

%files -n %{devname}
%doc README
%{_includedir}/%{name}/
%{_libdir}/%{name}.so
%{_datadir}/%{name}/src

#---------------------------------------------------------------------------

%if %{with python}
%package -n python-%{name}
Summary:		Python tools and interfaces for libsvm
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3dist(setuptools)
BuildRequires:	python3dist(scipy)
Requires:		svm-tools = %{version}-%{release}
#gnuplot is required by easy.py
Requires:		gnuplot

%description -n python-%{name}
Python tools and interfaces for libsvm.
Install this package if you want to develop
programs with libsvm in Python.

%files -n python-%{name}
%doc python/README-Python tools/README-Tools
%{libsvm_python_dir}
%{_bindir}/svm-*.py
%{python_sitearch}/libsvm.pth
%endif

#---------------------------------------------------------------------------

%if %{with java}
%package -n java-%{name}
Summary:		Java tools and interfaces for libsvm
BuildRequires:	java-devel
BuildRequires:	javapackages-tools
%if %{with maven}
BuildRequires:	maven-local
%endif
Requires:		java
Requires:		javapackages-tools
Requires:		svm-tools = %{version}-%{release}

Obsoletes:		libsvm-java < 2.88-1

%description -n java-%{name}
Java tools and interfaces for libsvm.
Install this package if you want to develop
programs with libsvm in Java.

%files -n java-%{name}
%doc java/README-Java
%{_javadir}/%{name}.jar
%endif

#---------------------------------------------------------------------------

%if %{with java}
%package javadoc
Summary:		Javadoc for libsvm
BuildRequires:	java-devel
BuildRequires:	javapackages-tools
BuildArch:		noarch
Requires:		java-%{name} = %{version}-%{release}

%description javadoc
Javadoc for libsvm.

%files javadoc
%{_javadocdir}/%{name}/
%endif

#---------------------------------------------------------------------------

%if %{with octave}
%package -n octave-%{name}
Summary:		Octave interface to libsvm
BuildRequires:	octave-devel
Requires:		svm-tools = %{version}-%{release}
Requires:		octave

%description -n octave-%{name}
Octave interface for libsvm.

%files -n octave-%{name}
%{octpkgdir}/
%endif

#---------------------------------------------------------------------------

%if %{with gtk}
%package svm-toy-gtk
Summary:		GTK version of svm-toy (libsvm demonstration program)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	desktop-file-utils
Requires:		gtk+2.0
Requires:		svm-tools = %{version}-%{release}

%description svm-toy-gtk
svm-toy is a libsvm demonstration program which has a gtk-GUI to
display the derived separating hyperplane.

%files svm-toy-gtk
%doc svm-toy/gtk/README
%{_bindir}/svm-toy-gtk
%{_datadir}/icons/hicolor/48x48/apps/%{name}-svm-toy-gtk-48.png
%{_datadir}/applications/*%{name}-svm-toy-gtk.desktop
%endif

#---------------------------------------------------------------------------

%if %{with qt}
%package svm-toy-qt
Summary:		QT version of svm-toy (libsvm demonstration program)
BuildRequires:	desktop-file-utils
BuildRequires:	qt5-qtbase-devel
Requires:		svm-tools = %{version}-%{release}

%description svm-toy-qt
svm-toy is a libsvm demonstration program which has a qt-GUI to
display the derived separating hyperplane.

%files svm-toy-qt
%doc svm-toy/qt/README
%{_bindir}/svm-toy-qt
%{_datadir}/icons/hicolor/48x48/apps/%{name}-svm-toy-qt-48.png
%{_datadir}/applications/*%{name}-svm-toy-qt.desktop
%endif

#---------------------------------------------------------------------------

%prep
%autosetup -p1
cp %{SOURCE1} ChangeLog
cp %{SOURCE2} .

%if %{with gtk}
cp %{SOURCE3} .
cp %{SOURCE5} %{name}-svm-toy-gtk-48.png
%endif
%if %{with qt}
cp %{SOURCE4} .
cp %{SOURCE5} %{name}-svm-toy-qt-48.png
# Fix the error: narrowing conversion
sed -e "s|{x,y,v}|{x,y,(signed char) v}|" \
	-e "s|{x,y,current_value}|{x,y,(signed char) current_value}|" \
	-e "s|(double)event->y()/YLEN, current_value|(double)event->y()/YLEN,(signed char) current_value|" \
	-i.narrowing svm-toy/qt/svm-toy.cpp
%endif

# Update the POM file, which is stuck on version 3.24
# pom_xpath_set does not work in rpm-4.11.1
# as it generated something like
# <version>
# <!-- begin of code added by maintainer -->
# 3.20
#
# <!-- end of code added by maintainer -->
# </version>
# Also, the latest pom added parent tags for org.sonatype.oss.oss-parent, which
# is deprecated and slated for removal from Fedora. It isn't needed, so remove
# it.
sed 's/%{pom_file_version}/%{version}/;/<parent>/,/<\/parent>/d' %{SOURCE5} > %{name}.pom

%if %{with maven}
%mvn_file %{maven_group_id}:%{name} %{maven_group_id}/%{name}
%endif

# Fix line endings
%{__sed} -i 's/\r//' FAQ.html
%{__sed} -i 's/\r//' ChangeLog

%build
%{set_build_flags}
# Build the library
make all RPM_CFLAGS="%{optflags}" LIBDIR="%{_libdir}" CPP_STD="%{cpp_std}" CXX=${CXX}

%if %{with java}
%if %{with maven}
%mvn_artifact %{name}.pom java/%{name}.jar
%endif
make svm-java JAVAC="%{javac}" JAR="%{jar}" RPM_CFLAGS="%{optflags}" CXX=${CXX}
cp README java/README-Java
%endif

%if %{with gtk}
make svm-gtk RPM_CFLAGS="%{optflags}" LIBDIR="%{_libdir}" CPP_STD="%{cpp_std}" CXX=${CXX}
cp README svm-toy/gtk
%endif

%if %{with qt}
make svm-toy-qt RPM_CFLAGS="%{optflags}" LIBDIR="%{_libdir}" CPP_STD="%{cpp_std}" CXX=${CXX} MOC_PATH="%{moc_path}"
cp README svm-toy/qt
%endif

%if %{with octave}
cd matlab
octave -H -q --no-window-system --no-site-file << EOF
make
EOF
cd -
%endif

%if %{with python}
make svm-python PYTHON_VERSION="%{pyver}" 
mv python/README python/README-Python
%endif

# README
mv tools/README tools/README-Tools

%install
%{set_build_flags}
%make_install LIBDIR=%{_libdir} LIBSVM_VER="%{version}" RPM_CFLAGS="%{optflags}" LIBDIR="%{_libdir}" CPP_STD="%{cpp_std}" CXX=${CXX}

ln -s %{name}.so.%{shver} %{buildroot}/%{_libdir}/%{name}.so

%if %{with python}
make install-python DESTDIR=%{buildroot} LIBDIR=%{_libdir} PYTHON_VERSION="%{pyver}"	
install -p -m 755 tools/*.py %{buildroot}%{python3_libsvm_dir}
for p in %{buildroot}%{python3_libsvm_dir}/*.py; do
	sed -i.orig -e 's|#!/usr/bin/env python|#!%{python3}|' $p
	touch -r $p.orig $p
	rm $p.orig
done
#chmod 0755 %{buildroot}%{python3_libsvm_dir}/{commonutil,svm,svmutil}.py
%endif

%if %{with java}
make install-java DESTDIR=%{buildroot} JAVA_TARGET_DIR="%{buildroot}%{_javadir}"
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -p -R java/docs/* %{buildroot}%{_javadocdir}/%{name}
%if %{with maven}
%mvn_install
%endif
%endif

%if %{with gtk}
make install-toy-gtk DESTDIR=%{buildroot}
%endif

%if %{with qt}
make install-toy-qt DESTDIR=%{buildroot}
%endif

%if %{with octave}
# FIXME: the *.mex files are arch-specific, so they should go into octpkglibdir
# like the *.oct files do. But octave refuses to load them from there. It will
# only load them if they are in octpkgdir. I don't know why.
mkdir -p %{buildroot}%{octpkgdir}/packinfo
cp -p matlab/*.mex %{buildroot}%{octpkgdir}
cp -p COPYRIGHT %{buildroot}%{octpkgdir}/packinfo/COPYING
cp -p %{SOURCE7} %{buildroot}%{octpkgdir}/packinfo/INDEX
cp -p %{SOURCE8} %{buildroot}%{octpkgdir}/packinfo/CITATION
sed 's/@VERSION@/%{version}/;s/@DATE@/%{release_date}/' %{SOURCE8} \
	> %{buildroot}%{octpkgdir}/packinfo/DESCRIPTION
cat > %{buildroot}%{octpkgdir}/packinfo/on_uninstall.m << EOF
function on_uninstall (desc)
  error ('Can not uninstall %%s installed by the redhat package manager', desc.name);
endfunction
EOF
%endif

# icons
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/48x48/apps/
%if %{with gtk}
cp %{name}-svm-toy-gtk-48.png %{buildroot}/%{_datadir}/icons/hicolor/48x48/apps/
%endif
%if %{with qt}
cp %{name}-svm-toy-qt-48.png %{buildroot}/%{_datadir}/icons/hicolor/48x48/apps/
%endif

# .desktop
mkdir -p %{buildroot}/%{_datadir}/applications
%if %{with gtk}
cp %{name}-svm-toy-gtk.desktop %{buildroot}/%{_datadir}/applications
%endif
%if %{with qt}
cp %{name}-svm-toy-qt.desktop %{buildroot}/%{_datadir}/applications
%endif

# [Bug 521194] Python: 'import libsvm' doesn't work
echo -e "# This file is not in the original libsvm tarball, but added for convenience of import libsvm.\n\
# This file is released under BSD license, just like the rest of the package.\n"\
 > %{buildroot}/%{libsvm_python_dir}/__init__.py

%if %{with gtk}
desktop-file-install --delete-original \
	--dir=%{buildroot}%{_datadir}/applications \
	%{buildroot}/%{_datadir}/applications/%{name}-svm-toy-gtk.desktop
%endif
%if %{with qt}
desktop-file-install --delete-original \
	--dir=%{buildroot}%{_datadir}/applications \
	%{buildroot}/%{_datadir}/applications/%{name}-svm-toy-qt.desktop \
%endif

# Fix Bug 646154 - libsvm-python's pth is not set correctly
echo 'libsvm' > %{buildroot}/%{python_sitearch}/libsvm.pth


%if %{with gtk}
%post svm-toy-gtk
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun svm-toy-gtk
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi
%endif

%if %{with octave}
%post -n octave-%{name}
%octave_cmd pkg rebuild
	
%preun -n octave-%{name}
%octave_pkg_preun

%postun -n octave-%{name}
%octave_cmd pkg rebuild
%endif
