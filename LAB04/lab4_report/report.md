1. mkdir lab4_report
2. cd lab4_report 
   touch report.md 
   mkdir files
   
   Часть 1
1. whoami > files/1_info.txt
pwd >> files/1_info.txt
uname -a >> files/1_info.txt
2. echo "fsdfsddfg
ahРоорорыав
ваыаып" > ~/secret.txt
3. chmod go-rw ~/secret.txt
4. cat ~/secret.txt > files/secret_backup.md
5. chmod 755 files/secret_backup.md
6. mv ~/secret.txt files/
7. sudo chown root:root files/secret_backup.md
8. ls /etc/host* > files/8_etc_hosts.txt 2>/dev/null || echo "Файлы не найдены" > files/8_etc_hosts.txt
9. sudo find /var/log -type f -mtime -7 > files/9_recent_logs.txt 2>/dev/null
    
    Часть 2
10. sudo useradd -m -s /bin/bash auditor
11. sudo usermod -aG sudo auditor
12. sudo passwd auditor
13. sudo su - auditor 
echo "Отчет аудитора системы" > /home/auditor/audit_report.txt
chmod 666 /home/auditor/audit_report.txt
exit
14. sudo cp /home/auditor/audit_report.txt files/14_audit_report.txt
sudo chown $USER:$USER files/14_audit_report.txt
15. sudo userdel -r auditor
16. cat /etc/passwd > files/16_users.txt

    Часть 3
17. sudo grep -r "localhost" /etc/ > files/17_localhost_files.txt 2>/dev/null
18. find /usr/bin -type f -executable -user root > files/18_root_binaries.txt 2>/dev/null
19. find ~ -type f -size +1M > files/19_large_files.txt 2>/dev/null
20. mkdir test_search
echo "port=8080" > test_search/data1.conf
echo "debug=true" > test_search/data2.conf
touch test_search/readme.txt
21. grep -l -E "port|debug" test_search/* > files/21_config_files.txt 2>/dev/null
22. find test_search -type f -empty -delete

    Часть 4
23. sleep 1h &
24. ps -u $USER > files/24_my_processes.txt
25. sleep_pid=$(pgrep sleep)
if [ ! -z "$sleep_pid" ]; then
    kill $sleep_pid
    echo "Процесс sleep с PID $sleep_pid завершен"
else
    echo "Процесс sleep не найден"
fi
26. sudo apt install htop
    htop
27. ps aux | grep systemd > files/27_systemd_processes.txt

    Часть 5
28. sudo tail -20 /var/log/syslog > files/28_syslog_tail.txt 2>/dev/null || echo "Файл не доступен" > files/28_syslog_tail.txt
29. sudo grep -i "failed" /var/log/auth.log > files/29_failed_logins.txt 2>/dev/null || echo "Файл не доступен" > files/29_failed_logins.txt
30. dpkg -l > files/30_installed_packages.txt
31. ss -tuln > files/31_open_ports.txt

    Часть 6
32. tar -czf lab4_files_backup.tar.gz files/
33. rm -rf files
    tar -xzf lab4_files_backup.tar.gz
34. cd ~
cp -r lab4_report lab4_final
35. rm -rf lab4_final
36. tree ~/lab4_report > files/36_tree.txt 2>/dev/null || ls -R lab4_report > files/36_tree.txt

