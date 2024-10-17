%define build_dvi 1

%define api		2.32
%define major		3
%define libdocument	%mklibname atrildocument %{major}
%define libview		%mklibname atrilview %{major}
%define girdocument	%mklibname atrildocument-gir %{api}
%define girview		%mklibname atrilview-gir %{api}
%define devname		%mklibname -d atril

Summary:	MATE Document viewer
Name:		mate-document-viewer
Version:	1.4.0
Release:	2
License:	GPLv2+ and GFDL+
Group:		Graphical desktop/GNOME
URL:		https://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz
Patch0:		mate-document-viewer-1.4.0-rosa-doc_buildfix.patch

BuildRequires:	docbook-dtd412-xml
BuildRequires:	ghostscript
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	mate-common
BuildRequires:	mate-conf
BuildRequires:	mate-icon-theme
BuildRequires:	xsltproc
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(ddjvuapi)
BuildRequires:	pkgconfig(gail)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libcaja-extension)
BuildRequires:	pkgconfig(libspectre)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(mateconf-2.0)
BuildRequires:	pkgconfig(mate-doc-utils)
BuildRequires:	pkgconfig(mate-icon-theme)
BuildRequires:	pkgconfig(mate-keyring-1)
BuildRequires:	pkgconfig(poppler-glib)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)

Requires:	ghostscript
Requires:	ghostscript-module-X

Provides:	atril = %{version}-%{release}

%description
Evince is the MATE Document viewer.
It supports PDF, PostScript and other formats.
To view .dvi files as produced by TeX in atril,
install the %{name}-dvi package.

%if %{build_dvi}
%package dvi
Summary:	TeX DVI document support for atril
Group:		Graphical desktop/GNOME
BuildRequires:	kpathsea-devel
#gw just like xdvi, needed for rendering the fonts
Requires:	texlive
Requires:	%{name} = %{version}-%{release}

%description dvi
This package adds support for displaying .dvi files to atril.
These files are 
produced by TeX, often using
a macro package like LaTeX.
%endif

%package -n %{libdocument}
Group:		System/Libraries
Summary:	MATE Document viewer library

%description -n %{libdocument}
This is the MATE Document viewer library, the shared parts of atril.

%package -n %{girdocument}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girdocument}
GObject Introspection interface description for %{name}.

%package -n %{libview}
Group:		System/Libraries
Summary:	MATE Document viewer library

%description -n %{libview}
This is the MATE Document viewer library, the shared parts of atril.

%package -n %{girview}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girview}
GObject Introspection interface description for %{name}.

%package -n %{devname}
Group:		Development/C
Summary:	MATE Document viewer library
Requires:	%{libdocument} = %{version}
Requires:	%{libview} = %{version}
Requires:	%{girdocument} = %{version}
Requires:	%{girview} = %{version}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This is the MATE Document viewer library, the shared parts of atril.

%prep
%setup -q
%apply_patches

%build
NOCONFIGURE=yes ./autogen.sh
%configure2_5x \
	--enable-tiff \
	--enable-djvu \
	--enable-comics \
%if %{build_dvi}
	--enable-dvi \
%endif
	--enable-gtk-doc \
	--enable-introspection \
	--disable-static \
	--disable-scrollkeueper \
	--disable-schemas-compile

make LIBS='-lm -lz -lgmodule-2.0'

%install
%makeinstall_std

desktop-file-edit --remove-category=MATE --add-category=X-MATE --add-category=2DGraphics %{buildroot}%{_datadir}/applications/atril.desktop

%find_lang atril --with-gnome

find %{buildroot} -name *.la -delete

%files -f atril.lang
%doc NEWS AUTHORS TODO
%{_sysconfdir}/mateconf/schemas/atril-thumbnailer-comics.schemas
%{_sysconfdir}/mateconf/schemas/atril-thumbnailer-djvu.schemas
%{_sysconfdir}/mateconf/schemas/atril-thumbnailer-dvi.schemas
%{_sysconfdir}/mateconf/schemas/atril-thumbnailer-ps.schemas
%{_sysconfdir}/mateconf/schemas/atril-thumbnailer.schemas
%{_bindir}/*
%{_libdir}/caja/extensions-2.0/libatril*so*
%dir %{_libdir}/atril/%{major}
%dir %{_libdir}/atril/%{major}/backends
%{_libdir}/atril/%{major}/backends/libcomicsdocument.so
%{_libdir}/atril/%{major}/backends/comicsdocument.atril-backend
%{_libdir}/atril/%{major}/backends/libdjvudocument.so
%{_libdir}/atril/%{major}/backends/djvudocument.atril-backend
%{_libdir}/atril/%{major}/backends/libpdfdocument.so
%{_libdir}/atril/%{major}/backends/pdfdocument.atril-backend
%{_libdir}/atril/%{major}/backends/libpsdocument.so
%{_libdir}/atril/%{major}/backends/psdocument.atril-backend
%{_libdir}/atril/%{major}/backends/libtiffdocument.so
%{_libdir}/atril/%{major}/backends/tiffdocument.atril-backend
%{_libexecdir}/atril-convert-metadata
%{_libexecdir}/atrild
%{_datadir}/applications/*
%{_datadir}/atril
%{_datadir}/dbus-1/services/org.mate.atril.Daemon.service
%{_datadir}/glib-2.0/schemas/org.mate.Atril.gschema.xml
%{_datadir}/MateConf/gsettings/atril.convert
%{_iconsdir}/hicolor/*/apps/atril*
%{_mandir}/man1/atril.1*
# mate help files
%{_datadir}/mate/help

%if %{build_dvi}
%files dvi
%{_libdir}/atril/%{major}/backends/libdvidocument.so
%{_libdir}/atril/%{major}/backends/dvidocument.atril-backend
%endif

%files -n %{libdocument}
%{_libdir}/libatrildocument.so.%{major}*

%files -n %{libview}
%{_libdir}/libatrilview.so.%{major}*

%files -n %{girdocument}
%{_libdir}/girepository-1.0/AtrilDocument-%{api}.typelib

%files -n %{girview}
%{_libdir}/girepository-1.0/AtrilView-%{api}.typelib

%files -n %{devname}
%{_datadir}/gtk-doc/html/atril
%{_datadir}/gtk-doc/html/libatrildocument-%{api}
%{_datadir}/gtk-doc/html/libatrilview-%{api}
%{_libdir}/libatrildocument.so
%{_libdir}/libatrilview.so
%{_libdir}/pkgconfig/atril*pc
%{_includedir}/atril*
%{_datadir}/gir-1.0/AtrilDocument-%{api}.gir
%{_datadir}/gir-1.0/AtrilView-%{api}.gir

