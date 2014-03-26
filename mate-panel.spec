%define url_ver %(echo %{version}|cut -d. -f1,2)

%define api	4
%define major	1
%define	gimajor	%{api}.0
%define libname	%mklibname mate-panel-applet %{api} %{major}
%define girname	%mklibname matepanelapplet-gir %{gimajor}
%define devname %mklibname -d mate-panel-applet

Summary:	The core programs for the MATE GUI desktop environment
Name:		mate-panel
Version:	1.8.0
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
Url:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	mandriva-panel.png

#BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	mate-common
#BuildRequires:	xsltproc
BuildRequires:	yelp-tools
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(mateweather)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libcanberra-gtk)
BuildRequires:	pkgconfig(libmate-menu)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libwnck-1.0)
BuildRequires:	pkgconfig(mate-desktop-2.0)
BuildRequires:	pkgconfig(NetworkManager)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xrandr)
Requires:	desktop-common-data
Requires:	mate-session-manager
Requires:	mate-desktop
Requires:	mate-menus
Requires:	mate-screensaver
Requires:	polkit-mate

Suggests:	mate-applets

%description
The MATE panel packages provides the mate panel, menus and some
basic applets for the panel.

%package -n	%{libname}
Summary:	%{summary}
Group:		System/Libraries

%description -n	%{libname}
Panel libraries for running MATE panels.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n	%{devname}
Summary:	Development libraries, include files for MATE panel
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	%{girname} = %{EVRD}

%description -n	%{devname}
Panel libraries and header files for creating MATE panels.

%prep
%setup -q
%apply_patches
NOCONFIGURE=yes ./autogen.sh

%build
%configure2_5x \
	--disable-static \
	--libexecdir=%{_libexecdir}/mate-applets \
	--enable-introspection \
	--with-in-process-applets=all

%make

%install
%makeinstall_std

# remove unneeded converters
rm -fr %{buildroot}%{_datadir}/MateConf

%find_lang %{name}-%{gimajor} --with-gnome --all-name

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp -a %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

%files -f %{name}-%{gimajor}.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/mate-desktop-item-edit
%{_bindir}/mate-panel
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/org.mate.panel.*.xml
%{_datadir}/mate-panel
%{_iconsdir}/hicolor/*/apps/*
%{_libdir}/%{name}/libclock-applet.so
%{_libdir}/%{name}/libfish-applet.so
%{_libdir}/%{name}/libnotification-area-applet.so
%{_libdir}/%{name}/libwnck-applet.so
%{_mandir}/man1/mate-desktop-item-edit.1*
%{_mandir}/man1/mate-panel.1*

%files -n %{libname}
%{_libdir}/libmate-panel-applet-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/MatePanelApplet-%{gimajor}.typelib

%files -n %{devname}
%doc ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_bindir}/mate-panel-test-applets
%{_mandir}/man1/mate-panel-test-applets.1*
%{_includedir}/*
%{_libdir}/libmate-panel-applet-%{api}.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/MatePanelApplet-%{gimajor}.gir

