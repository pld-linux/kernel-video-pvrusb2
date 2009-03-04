#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)

%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
%define		_enable_debug_packages	0

#
# main package.
#
%define		rel	0.1
%define		pname	kernel-video-pvrusb2
Summary:	Driver for Hauppauge WinTV PVR USB2 and similar devices
Name:       	%{pname}%{_alt_kernel}
Version:	20090115
Release:	%{rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://www.isely.net/downloads/pvrusb2-mci-%{version}.tar.bz2
# Source0-md5:	446c3b3498266ed551cdc94722fd1040
URL:		http://www.isely.net/pvrusb2/pvrusb2.html
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The pvrusb2 driver is designed for USB-hosted TV tuners which contain a
Conexant cx23416 (or similar) mpeg encoder chip. This encompasses a class of
USB analog and hybrid tuners which advertise the ability to encode video and
audio into an mpeg stream - directly in the hardware - an ideal feature for use
in PVR applications such as MythTV.

%prep
%setup -q -n pvrusb2-mci-%{version}

## prepare makefile:
#cat > path/to/dir/Makefile << EOF
#
#obj-m += pvrusb2.o MODULE2.o
#
#pvrusb2-objs := file1.o file2.o \
#	file3.o file4.o file5.o
#
#MODULE2-objs := file6.o file7.o file8.o
#
#CFLAGS += -DCONFIG_pvrusb2_SOME_OPTION=1
#%{?debug:CFLAGS += -DCONFIG_pvrusb2_DEBUG=1}
#EOF

%build
%build_kernel_modules -C driver -m pvrusb2

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -s standalone -n pvrusb2 -m driver/pvrusb2 -d kernel/video

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc doc/README doc/*.txt doc/*.html
/lib/modules/%{_kernel_ver}/kernel/video/*.ko*
%config(noreplace,missingok) %verify(not md5 mtime size) /etc/modprobe.d/*/*.conf
