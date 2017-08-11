20170709 django version 1.8.0
20170709 web: H5 CSS JS BOOTSTRAP3 BOOTSTRAP-TABLE BOOTSTRAP-DATETIMEPICKER BOOTSTRAP-SELECT KNOCKOUT TOASTR TITATOGGLE-DIST SUI.NAV 
20170709 update timeout to saltapi and add socket.onerror
20170713 upgrade v1 
20170713 fix bugs in upgrade about ConnectionError
20170714 update check app server and add refresh projects to saltstack_deploy
20170722 new add color_print.py to scripts
		 add redirect_url to logout
		 add access limit to user
		 set DEBUG = False in settings and add STATIC_ROOT
20170725 add detect
		 add iptables to saltstack_deploy and delete iptables from init
		 fix bugs in detect: add verfiy=False in requests.get
20170726 dbclick to edit tomcat_url and tomcat_project
		 add env={"LC_ALL": "zh_CN.UTF-8"} to ClientLocal in saltapi to fix chinese character encoding
20170728 add php to saltstack_deploy
20170729 set timeout for specific module['tomcat':1200, 'init':600, php':1800]
		 fix bug in saltstack.views add timeout=300 in if...else...
20170810 add salt_master_glb to check servers of shichang in check.py
		 update admin static files
		 add permission to user
		 update upgrade with will
20170811 在升级的js文件中添加对获取的IP地址进行数据类型判断