Name:		cyber-qrcode
# 1.9.<Build>
Version:	%{!?version:1.0.0}%{?version}
# ${commit_count}_git_${git_commit}
Release:	%{!?release:1}%{?release}
Summary:	Cyberlife QRcode API

Group:		Application
License:	GPL
URL:		http://www.cyber-life.cn/
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	python(abi) = 2.7
Requires:	systemd python(abi) = 2.7 nginx

%undefine __check_files

%description

%prep

%build
make

%install
make install DESTDIR=%{buildroot}

%post
systemctl daemon-reload

for svc in cyber-qrcode cyber-qrcode-swagger
do
	systemctl enable cyber-$svc.service
	systemctl restart cyber-$svc.service
done

systemctl enable nginx.service
systemctl restart nginx.service

%preun
for svc in auth-swagger auth-api ssdb-auth
do
	systemctl stop cyber-$svc.service
	systemctl disable cyber-$svc.service
done

%postun
/usr/bin/systemctl daemon-reload

%files
/etc/cyberlife/*
/etc/nginx/location.d/*
/opt/cyberlife/service/cyber-qrcode/*
/etc/systemd/system/*

%doc

%changelog
