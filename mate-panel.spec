%define url_ver %(echo %{version}|cut -d. -f1,2)

%define api	4
%define major	1

%define libname	%mklibname mate-panel-applet %{api} %{major}
%define devname %mklibname -d mate-panel-applet

%define	gimajor	%{api}.0
%define girname	%mklibname matepanelapplet-gir %{gimajor}

Summary:	The core programs for the MATE GUI desktop environment
Name:		mate-panel
Version:	1.18.7
Release:	2
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/Other
Url:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	mandriva-panel.png

BuildRequires:	intltool
BuildRequires:	mate-common
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(dconf)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0) 
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtk-doc)
BuildRequires:	pkgconfig(mateweather)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libcanberra-gtk3)
BuildRequires:	pkgconfig(libmate-menu)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libwnck-3.0)
BuildRequires:	pkgconfig(mate-desktop-2.0)
BuildRequires:	pkgconfig(NetworkManager)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	yelp-tools

Requires:	caja-schemas
Requires:	desktop-common-data
Requires:	mate-desktop
Requires:	mate-menus
Requires:	mate-session-manager
Requires:	mate-screensaver
Requires:	polkit-mate

Suggests:	mate-applets

%description
The MATE Desktop Environment is the continuation of GNOME 2. It provides an
intuitive and attractive desktop environment using traditional metaphors for
Linux and other Unix-like operating systems.

MATE is under active development to add support for new technologies while
preserving a traditional desktop experience.

This package provides the MATE panel, the libmate-panel-applet library and
several applets:

  * the MATE panel is the area on your desktop from which you can run
    applications and applets, and perform other tasks.

  * the libmate-panel-applet library allows to develop small applications
    which may be embedded in the panel. These are called applets.
    Documentation for the API is available with gtk-doc.

  * the applets supplied here include the Workspace Switcher, the Window
    List, the Window Selector, the Notification Area, the Clock and the
    infamous 'Wanda the Fish'.

%files -f %{name}.lang
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

#---------------------------------------------------------------------------

%package -n	%{libname}
Summary:	%{summary}
Group:		System/Libraries

%description -n	%{libname}
This package contains the shared libraries used by %{name}.

%files -n %{libname}
%{_libdir}/libmate-panel-applet-%{api}.so.%{major}*

#---------------------------------------------------------------------------

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
This package contains GObject Introspection interface library for %{name}.

%files -n %{girname}
%{_libdir}/girepository-1.0/MatePanelApplet-%{gimajor}.typelib

#---------------------------------------------------------------------------

%package -n	%{devname}
Summary:	Development libraries, include files for MATE panel
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	%{girname} = %{EVRD}

%description -n	%{devname}
This package contains libraries and includes files for developing programs
based on %{name}.

%files -n %{devname}
%doc ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_bindir}/mate-panel-test-applets
%{_mandir}/man1/mate-panel-test-applets.1*
%{_includedir}/*
%{_libdir}/libmate-panel-applet-%{api}.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/MatePanelApplet-%{gimajor}.gir

#---------------------------------------------------------------------------

%prep
%setup -q
%apply_patches

%build
#NOCONFIGURE=yes ./autogen.sh
%configure \
	--disable-schemas-compile \
	--enable-compile-warnings=no \
	--enable-gtk-doc \
	--libexecdir=%{_libexecdir}/mate-applets \
	--with-in-process-applets=all \
	%{nil}
%make

%install
%makeinstall_std

# add mandriva panel
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp -a %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

# locales
%find_lang %{name} --with-gnome --all-name

