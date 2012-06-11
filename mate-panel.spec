%define api	3
%define major	1
%define	girmajor	3.0
%define libname	%mklibname mate-panel-applet %{api} %{major}
%define libname2	%mklibname mate-panel-applet 2 %{major}
%define girname	%mklibname matepanelapplet-gir %{girmajor}
%define devname %mklibname -d mate-panel-applet

Summary:	The core programs for the MATE GUI desktop environment
Name:		mate-panel
Version:	1.2.1
Release:	3
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
Source1:	mandriva-panel.png

BuildRequires:	docbook-dtd412-xml
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libmatecomponent
BuildRequires:	mate-common
BuildRequires:	mate-conf
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(mateconf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(mateweather)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libcanberra-gtk)
#BuildRequires:	pkgconfig(libedataserverui-1.0)
BuildRequires:	pkgconfig(libmatecomponentui-2.0)
BuildRequires:	pkgconfig(libmate-menu)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libwnck-1.0)
BuildRequires:	pkgconfig(MateCORBA-2.0)
BuildRequires:	pkgconfig(mate-desktop-2.0)
BuildRequires:	pkgconfig(mate-doc-utils)
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

%package -n	%{libname2}
Summary:	%{summary}
Group:		System/Libraries

%description -n	%{libname2}
Panel libraries for running MATE panels.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n	%{devname}
Summary:	Development libraries, include files for MATE panel
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libname2} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}

%description -n	%{devname}
Panel libraries and header files for creating MATE panels.

%prep
%setup -q
%apply_patches

%build
NOCONFIGURE=yes ./autogen.sh
%configure2_5x \
	--disable-static \
	--libexecdir=/usr/lib/mate-applets \
	--enable-introspection  \
	--enable-matecomponent  \
	--disable-scrollkeeper \
	--disable-schemas-install

%make LIBS='-lgmodule-2.0'

%install
%makeinstall_std
find %{buildroot} -name '*.la' -delete;

%find_lang %{name}-3.0 --with-gnome --all-name

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp -a %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

%files -f %{name}-3.0.lang
%doc AUTHORS COPYING NEWS README
%{_sysconfdir}/mateconf/schemas/clock.schemas
%{_sysconfdir}/mateconf/schemas/fish.schemas
%{_sysconfdir}/mateconf/schemas/panel-compatibility.schemas
%{_sysconfdir}/mateconf/schemas/panel-default-setup.entries
%{_sysconfdir}/mateconf/schemas/panel-general.schemas
%{_sysconfdir}/mateconf/schemas/panel-global.schemas
%{_sysconfdir}/mateconf/schemas/panel-object.schemas
%{_sysconfdir}/mateconf/schemas/panel-toplevel.schemas
%{_sysconfdir}/mateconf/schemas/window-list.schemas
%{_sysconfdir}/mateconf/schemas/workspace-switcher.schemas
%{_bindir}/*
%{_libdir}/mate-panel/modules/libmate-panel-applets-matecomponent.so
%{_libexecdir}/mate-panel-add
%{_libexecdir}/clock-applet
%{_libexecdir}/fish-applet
%{_libexecdir}/notification-area-applet
%{_libexecdir}/wnck-applet
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/org.mate.panel.applet.ClockAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.FishAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.NotificationAreaAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.WnckletFactory.service
%{_datadir}/idl/mate-panel-2.0/MATE_Panel.idl
%{_datadir}/mate-panel
%{_datadir}/mate-panelrc
%{_datadir}/mate-2.0/ui/MATE_Panel_Popup.xml
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/*
# mate help files
%{_datadir}/mate/help/*

%files -n %{libname}
%{_libdir}/libmate-panel-applet-%{api}.so.%{major}*

%files -n %{libname2}
%{_libdir}/libmate-panel-applet-2.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/MatePanelApplet-%{girmajor}.typelib

%files -n %{devname}
%doc ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/libmate-panel*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/MatePanelApplet-%{girmajor}.gir

