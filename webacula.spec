Summary:	Web interface of a Bacula backup system
Summary(ru.UTF-8):	Веб интерфейс для Bacula backup system
Name:		webacula
Version:	5.0.3
Release:	0.1
License:	GPL v3+
Group:		Applications/WWW
URL:		http://webacula.sourceforge.net/
Source0:	http://downloads.sourceforge.net/webacula/%{name}-%{version}.tar.gz
# Source0-md5:	0a3b91e35d3bf55457f4c78b3882c2c2
Requires:	ZendFramework >= 1.8.3
Requires:	bacula-console >= 5.0
Requires:	php-gd
Requires:	php-json
Requires:	php-pcre
Requires:	php-pdo
Requires:	php-xml
Requires:	webserver
Requires:	webserver(php) >= 5.2.4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
rm -f ./application/.htaccess
rm -f ./html/test_mod_rewrite/.htaccess
rm -f ./html/.htaccess
rm -f ./install/.htaccess
rm -f ./languages/.htaccess
rm -f ./application/.htaccess
rm -f ./docs/.htaccess

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/application
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/html
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/languages
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/library
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/install

cp ./application/config.ini  $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config.ini
rm -f ./application/config.ini
ln -s %{_sysconfdir}/%{name}/config.ini  $RPM_BUILD_ROOT%{_datadir}/%{name}/application/config.ini

cp ./install/webacula.conf  $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/webacula.conf
rm -f ./install/webacula.conf

install -p ./install/webacula_clean_tmp_files.sh \
   $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/webacula_clean_tmp_files.sh
rm -f ./install/webacula_clean_tmp_files.sh

cp -pr ./application $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr ./html        $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr ./languages   $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr ./library     $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr ./install     $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(644,root,root,755)
%doc 4CONTRIBUTORS 4CONTRIBUTORS.ru AUTHORS COPYING README UPDATE ChangeLog
%doc docs/
%{_datadir}/%{name}/application
%{_datadir}/%{name}/html
%{_datadir}/%{name}/library
%{_datadir}/%{name}/install
/etc/cron.daily/webacula_clean_tmp_files.sh
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/languages
%config(noreplace) %{_sysconfdir}/httpd/conf.d/webacula.conf
%config(noreplace) %{_sysconfdir}/%{name}/config.ini
%lang(de) %{_datadir}/%{name}/languages/de
%lang(en) %{_datadir}/%{name}/languages/en
%lang(fr) %{_datadir}/%{name}/languages/fr
%lang(pt) %{_datadir}/%{name}/languages/pt
%lang(ru) %{_datadir}/%{name}/languages/ru
%lang(it) %{_datadir}/%{name}/languages/it
%lang(es) %{_datadir}/%{name}/languages/es
