%define shver 2
Name:           libsvm
Version:        3.17
Release:        2
Summary:        A Library for Support Vector Machines

License:        BSD
URL:            http://www.csie.ntu.edu.tw/~cjlin/libsvm/
Source0:        http://www.csie.ntu.edu.tw/~cjlin/libsvm/%{name}-%{version}.tar.gz
Source1:        http://www.csie.ntu.edu.tw/~cjlin/libsvm/log
Source2:        http://www.csie.ntu.edu.tw/~cjlin/papers/guide/guide.pdf
Source3:        libsvm-svm-toy-gtk.desktop
Source4:        libsvm-svm-toy-qt.desktop
Source5:        LibSVM-svm-toy-48.png
Source6:        %{name}.rpmlintrc
Patch0:         %{name}-%{version}.packageMain.patch
Patch1:         %{name}-%{version}.pythonDir.patch
Patch2:         %{name}-%{version}.javaDir.patch
Patch3:         %{name}-%{version}.svm-toy.patch
Patch4:         %{name}-%{version}.toolsDir.patch
BuildRequires:  grep

%{!?pyver: %define pyver %(python -c 'import sys; print(sys.version[0:3])')}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define libsvm_python_dir %{python_sitearch}/libsvm

%define javac javac
%define jar jar
%define libdir_libsvm %{_libdir}/libsvm
%define moc_path %{qt4dir}/bin/moc

%ifnarch ppc ppc64
%define no_java FALSE
%else
%define no_java NO_JAVA
Obsoletes: libsvm-java < 2.88-1
%endif

%description
LIBSVM is an integrated software for support vector classification,
(C-SVC, nu-SVC ), regression (epsilon-SVR, nu-SVR) and distribution
estimation (one-class SVM ). It supports multi-class classification.

%package devel
Summary:    Header file, object file, and source files of libsvm in C, C++ and Java

BuildRequires:  glibc-devel gawk
Requires:       %{name} = %{version}-%{release}

%description devel
Header file, object file of libsvm in C, C++ and Java.
Install this package if you want to develop programs with libsvm.


%package python
Summary:    Python tools and interfaces for libsvm

BuildRequires:  python-devel >= 2.4 gawk
#gnuplot is required by easy.py
Requires:       %{name} = %{version}-%{release}
Requires:       gnuplot

%description python
Python tools and interfaces for libsvm.
Install this package if you want to develop
programs with libsvm in Python.

%ifnarch ppc ppc64
%package java
Summary:    Java tools and interfaces for libsvm

BuildRequires:  java-devel >= 1.5.0
BuildRequires:  jpackage-utils

Requires:  java >= 1.5.0
Requires:  jpackage-utils
Requires:       %{name} = %{version}-%{release}

%description java
Java tools and interfaces for libsvm.
Install this package if you want to develop
programs with libsvm in Java.
%endif

%package svm-toy-gtk
Summary:    GTK version of svm-toy (libsvm demonstration program)

BuildRequires:  gtk+2.0-devel
BuildRequires:  desktop-file-utils
Requires:       gtk+2.0
Requires:       %{name} = %{version}-%{release}

%description svm-toy-gtk
svm-toy is a libsvm demonstration program which has a gtk-GUI to
display the derived separating hyperplane.

%package svm-toy-qt
Summary:    QT version of svm-toy (libsvm demonstration program)

BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig

BuildRequires:  qt4-devel
Requires:       %{name} = %{version}-%{release}

%description svm-toy-qt
svm-toy is a libsvm demonstration program which has a qt-GUI to
display the derived separating hyperplane.

%prep
%setup -q
%patch0 -p0 -b .packageMain
%patch1 -p0 -b .pythonDir
%patch2 -p0 -b .javaDir
%patch3 -p0 -b .svm-toy
%patch4 -p0 -b .toolsDir
cp %{SOURCE1} ChangeLog
cp %{SOURCE2} .
cp %{SOURCE3} .
cp %{SOURCE4} .
cp %{SOURCE5} %{name}-svm-toy-gtk-48.png
cp %{SOURCE5} %{name}-svm-toy-qt-48.png


%build
%{__sed} -i 's/\r//' FAQ.html
%{__sed} -i 's/\r//' ChangeLog
make all RPM_CFLAGS="$RPM_OPT_FLAGS" PYTHON_VERSION="%{pyver}" JAVAC="%{javac}" JAR="%{jar}" LIBDIR="%{_libdir}" MOC_PATH="%{moc_path}" NO_JAVA="%{no_java}"
mv python/README python/README-Python
mv tools/README tools/README-Tools
cp README java/README-Java
cp README svm-toy/gtk
cp README svm-toy/qt


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT LIBDIR=%{_libdir} PYTHON_VERSION="%{pyver}" LIBSVM_VER="%{version}"  NO_JAVA="%{no_java}" JAVA_TARGET_DIR="${RPM_BUILD_ROOT}/%{_javadir}"
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/src
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/48x48/apps/
cp %{name}-svm-toy-gtk-48.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/48x48/apps/
cp %{name}-svm-toy-qt-48.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/48x48/apps/
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
cp %{name}-svm-toy-gtk.desktop $RPM_BUILD_ROOT/%{_datadir}/applications
cp %{name}-svm-toy-qt.desktop $RPM_BUILD_ROOT/%{_datadir}/applications

%__ln_s %{name}.so.%{shver} $RPM_BUILD_ROOT/%{_libdir}/%{name}.so


# [Bug 521194] Python: 'import libsvm' doesn't work
echo -e "# This file is not in the original libsvm tarball, but added for convenience of import libsvm.\n\
# This file is released under BSD license, just like the rest of the package.\n"\
 > $RPM_BUILD_ROOT/%{libsvm_python_dir}/__init__.py

desktop-file-install --delete-original \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
  ${RPM_BUILD_ROOT}/%{_datadir}/applications/%{name}-svm-toy-gtk.desktop \
  ${RPM_BUILD_ROOT}/%{_datadir}/applications/%{name}-svm-toy-qt.desktop \

# Fix Bug 646154 - libsvm-python's pth is not set correctly
echo 'libsvm' > $RPM_BUILD_ROOT/%{python_sitearch}/libsvm.pth

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

%files
%doc COPYRIGHT FAQ.html ChangeLog guide.pdf
%{_bindir}/svm-predict
%{_bindir}/svm-scale
%{_bindir}/svm-train
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/examples
%{_libdir}/%{name}.so.%{shver}

%files devel
%doc README
%{_includedir}/%{name}/
%{_libdir}/%{name}.so

%files python
%doc python/README-Python tools/README-Tools
%{libsvm_python_dir}
%{_bindir}/svm-*.py
%{python_sitearch}/libsvm.pth

%ifnarch ppc ppc64
%files java
%doc java/README-Java java/test_applet.html
%{_javadir}/%{name}.jar
%endif

%files svm-toy-gtk
%doc svm-toy/gtk/README
%{_bindir}/svm-toy-gtk
%{_datadir}/icons/hicolor/48x48/apps/%{name}-svm-toy-gtk-48.png
%{_datadir}/applications/*%{name}-svm-toy-gtk.desktop

%files svm-toy-qt
%doc svm-toy/qt/README
%{_bindir}/svm-toy-qt
%{_datadir}/icons/hicolor/48x48/apps/%{name}-svm-toy-qt-48.png
%{_datadir}/applications/*%{name}-svm-toy-qt.desktop
