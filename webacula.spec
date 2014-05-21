# TODO
# - fails to work if some %lang file not installed
# - does not work with baucla 5.2:
#   PHP Fatal error:  Uncaught exception 'Zend_Exception' with message 'Version error for Catalog database (wanted 12, got 14) ' in /usr/share/webacula/html/index.php:183\nStack trace:\n#0 {main}\n  thrown in /usr/share/webacula/html/index.php on line 183
%define		php_min_version 5.2.4
# - Requires: /bin/bash
%include	/usr/lib/rpm/macros.php
Summary:	Web interface of a Bacula backup system
Summary(ru.UTF-8):	Веб интерфейс для Bacula backup system
Name:		webacula
Version:	5.5
Release:	0.2
License:	GPL v3+
Group:		Applications/WWW
URL:		http://webacula.sourceforge.net/
Source0:	http://downloads.sourceforge.net/webacula/%{name}-%{version}.tar.gz
# Source0-md5:	d7f5256247836ddc663a6313e3c019d2
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	ZendFramework >= 1.8.3
Requires:	bacula-console >= 5.0
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php(dom)
Requires:	php(gd)
Requires:	php(json)
Requires:	php(pcre)
Requires:	php(pdo)
Requires:	php(xml)
Requires:	webapps
Requires:	webserver(php) >= 5.2.4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Webacula - Web Bacula - web interface of a Bacula backup system.
Supports the run Job, restore all files or selected files, restore the
most recent backup for a client, restore backup for a client before a
specified time, mount/umount Storages, show scheduled, running and
terminated Jobs and more. Supported languages: English, French,
German, Italian, Portuguese Brazil, Russian.

%description -l ru.UTF-8
Webacula - Web Bacula - веб интерфейс для Bacula backup system.
Поддерживает запуск Заданий, восстановление всех или выбранных файлов,
восстановление самого свежего бэкапа для клиента, восстановление
бэкапа для клиента сделанного перед указанным временем,
монтирование/размонтирование Хранилищ, показ запланированных,
выполняющихся и завершенных Заданий и прочее. Поддерживаемые языки:
английский, французский, немецкий, итальянский, бразильский
португальский, русский.

%prep
%setup -q
#%{__rm} application/.htaccess
%{__rm} html/test_mod_rewrite/.htaccess
%{__rm} html/.htaccess
%{__rm} install/.htaccess
%{__rm} languages/.htaccess
%{__rm} application/.htaccess
%{__rm} docs/.htaccess

%{__rm} application/config.ini.original

%{__rm} languages/*/*.po

# php 5.3 specific __DIR__ can be easily backported
%{__sed} -i -e 's#__DIR__#dirname(__FILE__)#g' html/index.php

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/{application,html,languages,library,install}} \
	$RPM_BUILD_ROOT/etc/cron.daily \

cp -a application html languages library install $RPM_BUILD_ROOT%{_appdir}

mv $RPM_BUILD_ROOT{%{_appdir}/application,%{_sysconfdir}}/config.ini
ln -s %{_sysconfdir}/config.ini $RPM_BUILD_ROOT%{_appdir}/application
mv $RPM_BUILD_ROOT{%{_appdir}/install/apache/webacula.conf,%{_sysconfdir}/apache.conf}
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf
#mv $RPM_BUILD_ROOT{%{_appdir}/install,/etc/cron.daily}/webacula_clean_tmp_files.sh

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc 4CONTRIBUTORS 4CONTRIBUTORS.ru AUTHORS COPYING README UPDATE ChangeLog
%doc docs
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.ini
#%attr(755,root,root) /etc/cron.daily/webacula_clean_tmp_files.sh
%dir %{_appdir}
%{_appdir}/application
%{_appdir}/html
%{_appdir}/library
%{_appdir}/install
%dir %{_appdir}/languages
%lang(de) %{_appdir}/languages/de
%lang(en) %{_appdir}/languages/en
%lang(fr) %{_appdir}/languages/fr
%lang(pt) %{_appdir}/languages/pt
%lang(ru) %{_appdir}/languages/ru
%lang(it) %{_appdir}/languages/it
%lang(es) %{_appdir}/languages/es
%lang(cs) %{_appdir}/languages/cs
