$(function () {
    tableInit.Init();
    operate.operateInit();
});

//全局变量
window.run = true;
window.postUpgradeDate = {
        svn_id:'',
        tag:'',
        project:'',
        ip_addr:[],
        act:'',
        step:0,
        envir:'',
        restart:'',
},
window.uat_ip_addr_list = new Array();
window.online_ip_addr_list = new Array();
window.html_uat = "";
window.html_online = "";
window.modal_results = document.getElementById("upgrade_results");
window.modal_head_content = document.getElementById("upgrade_modal_head_content");
window.modal_head_close = document.getElementById("upgrade_modal_head_close");
window.upgrade_progress_head = document.getElementById("upgrade_progress_head");
window.upgrade_progress_body = document.getElementById("upgrade_progress_body");

var tableInit = {
    Init: function () {
        this.operateFormatter;
        this.cur_statusFormatter;
        this.dbclick();
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: '/upgrade/query_svn',         //请求后台的URL（*）
            method: 'post',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset, 'act':'query_not_deleted' };
            },//传递参数（*）
            toolbarAlign: "left",
            columns: [
                //{ 
                //    checkbox: true 
                //},
                {
                    field: 'id',
                    title: 'id',
                    sortable: true,
                    width:'1%',
                    //align: 'center'
                },{
                    field: 'id_time',
                    title: '版本时间',
                    sortable: true,
                    //align: 'center',
                    width:'9%',
                },{
                    field: 'svn_id',
                    title: '版本',
                    sortable: true,
                    width:'6%',
                    //align: 'center'
                },{
                    field: 'tag',
                    title: '标签',
                    sortable: true,
                    width:'5%',
                    //align: 'center'
                },{
                    field: 'project',
                    title: '项目名',
                    sortable: true,
                    width:'18%',
                    //align: 'center'
                },{
                    field: 'cur_status',
                    title: '状态',
                    sortable: true,
                    width:'6%',
                    //align: 'center',
                    //events: this.cur_statusEvents,
                    formatter: this.cur_statusFormatter
                },{
                    field: 'info',
                    title: '备注',
                    sortable: true,
                    //align: 'center',
                    width:'9%',
                },{
                    field: 'operations',
                    title: '操作项',
                    //align: 'center',
                    width:'9%',
                    events: operateEvents,
                    formatter: this.operateFormatter,
                    //width:300,
                },
            ]

        });
        ko.applyBindings(this.myViewModel, document.getElementById("upgrade_op_table"));
    },

    dbclick: function (){
        $('#upgrade_op_table').on('all.bs.table', function (e, name, args) {
            //console.log('Event:', name, ', data:', args);
        }).on('dbl-click-cell.bs.table', function (e, field, value, row, $element) {
            if (row.deleted == 1){
                alert(row.svn_id+': 是删除的状态，请先恢复！')
                return false;
            }

            $('#upgrade_modal').modal('show');
            upgrade_parms = {
                id_time:row.id_time,
                svn_id:row.svn_id,
                tag:row.tag,
                cur_status,
                project:row.project,
            }

            if (row.cur_status == 'done'){
                upgrade_parms.cur_status = ko.observable('已升级');
            }else if (row.cur_status == 'undone'){
                upgrade_parms.cur_status = ko.observable('未升级');
            }else if (row.cur_status == 'rollback'){
                upgrade_parms.cur_status = ko.observable('已回退');
            }

            //初始化升级按钮
            operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip','upgrade_interrupt'], true);
            //if (row.cur_status == 'done'){
            //    document.getElementById('upgrade_deploy').disabled = false;
            //    document.getElementById('upgrade_diff').disabled = false;
            //    document.getElementById('upgrade_rollback').disabled = false;
            //    document.getElementById('upgrade_interrupt').disabled = true;
            //}else if (row.cur_status == 'undone'){
            //    document.getElementById('upgrade_deploy').disabled = false;
            //    document.getElementById('upgrade_diff').disabled = false;
            //    document.getElementById('upgrade_rollback').disabled = false;
            //    document.getElementById('upgrade_interrupt').disabled = true;
            //}else if (row.cur_status == 'rollback'){
            //    document.getElementById('upgrade_deploy').disabled = false;
            //    document.getElementById('upgrade_diff').disabled = false;
            //    document.getElementById('upgrade_rollback').disabled = true;
            //    document.getElementById('upgrade_interrupt').disabled = true;
            //}

            //初始化页面参数
            var obj_envir = document.getElementsByName('upgrade_envir');
            var obj_restart = document.getElementsByName('upgrade_restart');
            for(i=0;i<obj_envir.length;i++) { 
                if(obj_envir[i].checked) { 
                    obj_envir[i].checked = false; 
                } 
            }
            for(i=0;i<obj_restart.length;i++) { 
                if(obj_restart[i].checked) { 
                    obj_restart[i].checked = false; 
                } 
            }
            document.getElementById('upgrade_ip').innerHTML = "";
            $('.selectpicker').selectpicker('refresh');
            operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
            upgrade_progress_body.hidden = true;
            upgrade_progress_head.innerHTML= "";
            modal_head_content.innerHTML = "请选择升级参数";
            modal_head_close.innerHTML = "&times;";
            modal_results.innerHTML = "";
            operate.DisSelectedIp();
            ko.cleanNode(document.getElementById("upgrade_modal_body"));
            ko.applyBindings(upgrade_parms, document.getElementById("upgrade_modal_body"));
            operate.GetProjectServers(row.project);
        });
    },

    operateFormatter: function (value,row,index){
        if (row.deleted == 0){
            content_n = [
                '<a class="delete text-info" href="javascript:void(0)" title="删除">',
                    '删除',
                '</a>',
            ].join('');
        }else if (row.deleted == 1){
            content_n = [
                '<a class="recover text-info" href="javascript:void(0)" title="恢复">',
                    '恢复',
                '</a>',
            ].join('');
        }else {
            content_n = "";
        }

        var content = [
            '<a class="upgrade text-info" href="javascript:void(0)" title="升级">',
                '升级',
            '</a>&ensp;',
            '<a class="diff text-primary" href="javascript:void(0)" title="比对代码">',
                '比对',
            '</a>&ensp;',
        ].join('');
        if (row.cur_status == 'rollback' || row.cur_status == 'undone'){
        }else {
            content = content + [
            '<a class="rollback text-muted" href="javascript:void(0)" title="回退">',
                '回退',
            '</a>'
            ].join('');   
        }
        return content_n;
    },

    cur_statusFormatter: function (value,row,index) {
        var status = row.cur_status;
        var content = "";
        if (status == 'undone'){
            content = '<span style="background-color: #FF0000">未升级</span>';
            return content;
        }else if(status == 'done'){
            content = '<span style="background-color: #32CD32">已升级</span>';
            return content;
        }else if(status == 'rollback'){
            content = '<span style="background-color: #FFD700">已回退</span>';
            return content;
        }else {
            return "未定义";
        }

    },
};

window.operateEvents = {
    'click .upgrade': function (e, value, row, index) {
        var tmp = document.getElementById("OperateUpgraderesults");
        var tmpfooter = document.getElementById("progressFooter");
        tmp.innerHTML = "";
        tmpfooter.innerHTML = "";
        var socket = new WebSocket("ws://" + window.location.host + "/upgrade/operate_upgrade");
        socket.onopen = function () {
            console.log('WebSocket open');//成功连接上Websocket
            //socket.send($('#message').val());//发送数据到服务端
        };
        socket.onerror = function (){
            alert('连接服务器失败，请重试！');
            return false;
        };
        socket.onmessage = function (e) {
            data = eval('('+ e.data +')')
            //console.log('message: ' + data.message);//打印服务端返回的数据
            $('#OperateUpgraderesults').append('<p>' + data.message + '</p>');
            var a = document.getElementById("progress_head");
            a.innerHTML = "操作进行中，请勿刷新页面......";
            $("#progress_bar").css("width", "30%");
            p = 0;  
            stop = 0; 
            $('#runprogress').modal('show');  
            run(data.count); 
            if (data.count == 5){
                //$('#runprogress').modal('hide'); 
                console.log('websocket已关闭');
                tmpfooter.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span>关闭</button>'
            }
        }; 
        return false;
    },
    'click .diff': function (e, value, row, index) {
        console.log('click diff. '+row.project+" "+row.cur_status)
        return false;
    },
    'click .rollback': function (e, value, row, index) {
        console.log('click rollback. '+row.project+" "+row.cur_status)
        return false;
    },
    'click .delete': function (e, value, row, index) {
        $('#upgrade_op_table').bootstrapTable('remove', {
                field: 'id',
                values: [row.id]
        });
        var postData = {};
        postData['deleted'] = 1
        postData['id'] = row.id
        postData['svn_id'] = row.svn_id

        $.ajax({
            url: "/upgrade/update_svn",
            type: "post",
            data: JSON.stringify(postData),
            success: function (datas, status) {
                if (datas == 'failure'){
                    alert("failure");
                }else {
                    toastr.warning('删除成功！', row.project+": "+row.svn_id)
                }
            },
            error:function(msg){
                alert("删除失败，请检查日志！");
            }
        });
        return false;
    },
    'click .recover': function (e, value, row, index) {
        var postData = {};
        postData['deleted'] = 0
        postData['id'] = row.id
        postData['svn_id'] = row.svn_id

        $.ajax({
            url: "/upgrade/update_svn",
            type: "post",
            data: JSON.stringify(postData),
            success: function (datas, status) {
                if (datas == 'failure'){
                    alert("failure");
                }else {
                    toastr.warning('恢复成功！', row.project+": "+row.svn_id)
                    $('#upgrade_op_table').bootstrapTable('refresh');
                }
            },
            error:function(msg){
                alert("恢复失败，请检查日志！");
            }
        });
        
        return false;
    }
};  

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.operateUpgradeSelect();
        this.upgradeButtons();
        //this.setHandleUser();
        //this.selectpicker();
    },

    getpostData: function (act) {
        var obj_envir = document.getElementsByName('upgrade_envir');
        var obj_restart = document.getElementsByName('upgrade_restart');
        for(i=0;i<obj_envir.length;i++) { 
            if(obj_envir[i].checked) { 
                postUpgradeDate.envir = obj_envir[i].value; 
            } 
        }
        postUpgradeDate.restart = '';
        for(i=0;i<obj_restart.length;i++) { 
            if(obj_restart[i].checked) { 
                postUpgradeDate.restart = obj_restart[i].value; 
            } 
        }
        postUpgradeDate.svn_id = upgrade_parms.svn_id;
        postUpgradeDate.tag = upgrade_parms.tag;
        postUpgradeDate.project = upgrade_parms.project;
        postUpgradeDate.act = act;
        var selectedValue = []; 
        var objSelect = document.getElementById('upgrade_ip');
        for(var i = 0; i < objSelect.options.length; i++) { 
            if (objSelect.options[i].selected == true) 
            selectedValue.push(objSelect.options[i].value);
        }
        if (selectedValue.length == 0 && postUpgradeDate.envir == 'UAT'){
            postUpgradeDate.ip_addr = uat_ip_addr_list;
        }else if (selectedValue.length == 0 && postUpgradeDate.envir == 'ONLINE') {
            postUpgradeDate.ip_addr = online_ip_addr_list;
        }else {
            postUpgradeDate.ip_addr = selectedValue;
        }
        return postUpgradeDate;
    },

    disableButtons: function (buttonList, fun) {
        for (var i = 0; i < buttonList.length; i++){
            if (fun){
                document.getElementById(buttonList[i]).disabled = true;
            }else {
                document.getElementById(buttonList[i]).disabled = false;
            }
        }
    },

    upgradeButtons: function(){
        $('#upgrade_deploy').on("click", function () {
            var args = {};

            args['act'] = 'deploy';
            args['content1'] = '升级中';
            args['content2'] = '升级完成';
            //console.log(args.act)
            operate.socketConn(args);

        });

        $('#upgrade_diff').on("click", function () {
            var args = {};

            args['act'] = 'diff';
            args['content1'] = '对比中';
            args['content2'] = '对比完成';
            //console.log(args.act)

            operate.socketConn(args);

        });

        $('#upgrade_rollback').on("click", function () {
            var args = {};

            args['act'] = 'rollback';
            args['content1'] = '回退中';
            args['content2'] = '回退完成';
            //console.log(args.act)
            operate.socketConn(args);
        });



        $('#upgrade_interrupt').on("click", function () {
            //alert('终止')
            cur_status.innerHTML = '中断';
            modal_head_content.innerHTML = "中断";
            run = false;
            operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
            operate.disableButtons(['upgrade_interrupt'], true);
        });
    },

    GetCheckedEnvir: function (){
        var obj_envir = document.getElementsByName('upgrade_envir');
        for(i=0;i<obj_envir.length;i++) { 
            if(obj_envir[i].checked) { 
                return obj_envir[i].value;
            } 
        }
        return false;
    },

    socketConn: function (args){
        //获取需要post的所有数据
        var postData = operate.getpostData(args.act);
        if (postData.ip_addr.length == 0){
            alert('所选IP为空，请检查！');
            return false;
        }
        if ((postData.act == 'deploy' || postData.act == 'rollback') && postData.restart == ''){
            alert('请选择是否重启服务！');
            return false;
        }

        postData.envir = operate.GetCheckedEnvir()
        postData.step = 0;
        run = true;

        //更改页面展示的状态
        modal_head_content.innerHTML = args.content1+"，请勿刷新页面......";
        cur_status = document.getElementById('cur_status');
        cur_status.innerHTML = args.content1;
        modal_head_close.innerHTML = "";
        upgrade_progress_body.hidden = false;
        $("#upgrade_progress_bar").css("width", "0%");

        //按钮禁用
        operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], true);

        //插入结果
        upgrade_progress_head.innerHTML="总共：<strong>"+postData.ip_addr.length+"</strong>台    "+"成功：<strong>"+postData.step+"</strong>台";
        
        if (postData.step == postData.ip_addr.length - 1){
            operate.disableButtons(['upgrade_interrupt'], true);
        }else {
            operate.disableButtons(['upgrade_interrupt'], false);
        }
        //建立socket连接
        var socket = new WebSocket("ws://" + window.location.host + "/upgrade/op_upgrade/deploy");
        socket.onopen = function () {
            //第一次发送数据
            socket.send(JSON.stringify(postData));
            $('#upgrade_results').append('<p>执行动作:&thinsp;<strong>'+ postData.act +'</strong></p>');
            $('#upgrade_results').append('<p>返回结果:</p>');
        };
        socket.onerror = function (){
            modal_head_content.innerHTML = '与服务器连接失败...';
            upgrade_progress_head.innerHTML = '与服务器连接失败...';
            modal_head_close.innerHTML = "&times;";
            operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
            operate.disableButtons(['upgrade_interrupt'], true);
        };
        socket.onmessage = function (e) {
            //return false;
            data = eval('('+ e.data +')')

            if (data.op_status == -1){
                modal_head_close.innerHTML = "&times;"
                operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
                operate.disableButtons(['upgrade_interrupt'], true);
                $('#upgrade_results').append('<p>传入参数错误，请检查服务！</p>');
                return false;
            }else if (data.op_status == 0){
                modal_head_close.innerHTML = "&times;"
                operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
                operate.disableButtons(['upgrade_interrupt'], true);
                $('#upgrade_results').append('<p>错误：'+ data.result +'</p>');
                return false;
            }

            if (data.act == 'getfile'){
                if (data.result == 'ReadTimeout' || data.result == 'UnknownError' || data.result == 'ConnectionError' || data.result == 'InsertRecordError'){
                    modal_head_close.innerHTML = "&times;"
                    $('#upgrade_results').append('<p>获取svn版本文件: '+ data.result +'</p>');
                    operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
                    return false;
                }else {
                    $('#upgrade_results').append('<p>获取svn版本文件: 成功</p>');
                    postData.step = postData.step + 1;
                    socket.send(JSON.stringify(postData));
                    return false;
                }
            }

            var button = ""
            var button_html = "";
            //console.log('ip_addr: ' + data.ip_addr);//打印服务端返回的数据
            var timestamp = operate.getNowFormatDate('timestamp')
            var width = 100*(data.step+1)/postData.ip_addr.length + "%"
            postData.step = postData.step + 1;
            if (postData.step == postData.ip_addr.length - 1){
                operate.disableButtons(['upgrade_interrupt'], true);
            }
            $("#upgrade_progress_bar").css("width", width);
            $('#upgrade_results').append('<p><strong>'+data.ip_addr[data.step-1]+'</strong></p>');
            $('#upgrade_results').append('<pre class="pre-scrollable"><xmp>'+data.result+'</xmp></pre>',)
            upgrade_progress_head.innerHTML="总共：<strong>"+postData.ip_addr.length+"</strong>台    "+"成功：<strong>"+(data.step)+"</strong>台";
            //console.log(data.step+" : "+postData.ip_addr.length)
            if (run){
                if (data.step <= postData.ip_addr.length - 1){
                    //console.log(postData);
                    socket.send(JSON.stringify(postData));
                }else {
                    cur_status.innerHTML = args.content2;
                    modal_head_close.innerHTML = "&times;"
                    modal_head_content.innerHTML = args.content2;
                    operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
                    operate.disableButtons(['upgrade_interrupt'], true);
                    //socket.close();
                }
            }else {
                modal_head_close.innerHTML = "&times;"
                operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
                operate.disableButtons(['upgrade_interrupt'], true);
                //socket.close();
            }
            
        }; 
        return false;
    },

    getNowFormatDate: function (type) {
        var seperator1 = "-";
        var seperator2 = ":";
        var dtCur = new Date();
        var yearCur = dtCur.getFullYear();
        var monCur = dtCur.getMonth() + 1;
        var dayCur = dtCur.getDate();
        var hCur = dtCur.getHours();
        var mCur = dtCur.getMinutes();
        var sCur = dtCur.getSeconds();
        var currentdate = yearCur + seperator1 + (monCur < 10 ? "0" + monCur : monCur) + seperator1 + (dayCur < 10 ? "0" + dayCur : dayCur) + " " + (hCur < 10 ? "0" + hCur : hCur) + seperator2 + (mCur < 10 ? "0" + mCur : mCur) + seperator2 + (sCur < 10 ? "0" + sCur : sCur);
        var timestamp = yearCur + (monCur < 10 ? "0" + monCur : monCur) + (dayCur < 10 ? "0" + dayCur : dayCur) + (hCur < 10 ? "0" + hCur : hCur) + (mCur < 10 ? "0" + mCur : mCur) + (sCur < 10 ? "0" + sCur : sCur);
        if (type == 'normal'){
            return currentdate;
        }else if (type = 'timestamp'){
            return timestamp;
        }   
    },

    DisSelectedIp: function (){
        var obj = operate.GetCheckedEnvir()
        var selectedValue = []; 
        var objSelect = document.getElementById('upgrade_ip'); 
        for(var i = 0; i < objSelect.options.length; i++) { 
            if (objSelect.options[i].selected == true) 
            selectedValue.push(" "+objSelect.options[i].value);
        }
        var selected_ip = selectedValue;
        if (obj == 'UAT'){
            if (selected_ip.length == 0 && uat_ip_addr_list.length != 0){
                selected_ip = 'All';
            }else if (selected_ip.length == 0 && uat_ip_addr_list.length == 0){
                selected_ip = 'Null';
            }
        }else if (obj == 'ONLINE'){
            if (selected_ip.length == 0 && online_ip_addr_list.length != 0){
                selected_ip = 'All';
            }else if (selected_ip.length == 0 && online_ip_addr_list.length == 0){
                selected_ip = 'Null';
            }
        }else {
            selected_ip = 'Null';
        }
        if (selected_ip.length > 6){
                selected_ip = selected_ip.splice(0, 6);
                selected_ip = selected_ip + ' ...';
        }

        ko.cleanNode(document.getElementById("selected_ip"));
        ko.applyBindings(selected_ip, document.getElementById("selected_ip"));
    },

    GetProjectServers: function(project){
        uat_ip_addr_list.length = 0;
        online_ip_addr_list.length = 0;
        html_uat = "";
        html_online = "";
        var projectlist = [];
        projectlist.push(project);
        //console.log(projectlist);
        var postData = {};
        postData['project'] = projectlist;
        $.ajax({
            url: "/saltstack/restart/get_project_servers",
            type: "post",
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(postData),
            success: function (datas, status) {
                //alert(datas);
                var data = eval(datas);
                //var html = "<option value=''></option>";
                
                for (var project in data){
                    var html_uat_tmp = "";
                    var html_online_tmp = "";
                    $.each(data[project], function (index, item) { 
                        //循环获取数据 
                        var name = data[project][index];
                        html_name = "<option value='"+name.ip_addr+"' data-subtext='"+name.info+" "+name.role+"'>"+name.ip_addr+"</option>";
                        if (name.envir == 'UAT'){
                            html_uat_tmp = html_uat_tmp + html_name;
                            uat_ip_addr_list.push(name.ip_addr);
                        }else if (name.envir == 'ONLINE'){
                            html_online_tmp = html_online_tmp + html_name;
                            online_ip_addr_list.push(name.ip_addr);
                        }
                    }); 
                    //html_tmp = "<optgroup label='"+ project +"'>" + html_tmp + "</optgroup>";
                    html_uat = html_uat + html_uat_tmp;
                    html_online = html_online + html_online_tmp;
                }
                //document.getElementById('upgrade_ip').innerHTML=html;
                //$('.selectpicker').selectpicker({title:"请选择服务器地址"});
                //$('.selectpicker').selectpicker('refresh');
                return false;
            },
            error:function(msg){
                alert("获取项目服务器地址失败！");
                return false;
            }
        });
    },

    setupIp: function (obj){
        if (obj.value == 'UAT'){
            document.getElementById('upgrade_ip').innerHTML=html_uat;
        }else if(obj.value == 'ONLINE'){
            document.getElementById('upgrade_ip').innerHTML=html_online;
        }
        $('.selectpicker').selectpicker('refresh');
        operate.DisSelectedIp();
    },

    operateUpgradeSelect: function(){
        $('#btn_op_search').on("click", function () {
            var postData = {
                project:"all",
                cur_status_sel:"all",
                deleted:"all",
            };
            if (! document.getElementById("project_active").value == ""){
                var projectlist = [];
                var objSelectproject = document.upgradeform.project_active; 
                for(var i = 0; i < objSelectproject.options.length; i++) { 
                    if (objSelectproject.options[i].selected == true) 
                    projectlist.push(objSelectproject.options[i].value);
                }
                postData['project'] = projectlist;
            }
            if (document.getElementById("cur_status_sel").value != ""){
                var statuslist = [];
                var objSelectstatus = document.upgradeform.cur_status_sel; 
                for(var i = 0; i < objSelectstatus.options.length; i++) { 
                    if (objSelectstatus.options[i].selected == true) 
                    statuslist.push(objSelectstatus.options[i].value);
                }
                postData['cur_status_sel'] = statuslist;
            }
            if (document.getElementById("deleted").value != ""){
                var deletedlist = [];
                var objSelectstatus = document.upgradeform.deleted; 
                for(var i = 0; i < objSelectstatus.options.length; i++) { 
                    if (objSelectstatus.options[i].selected == true) 
                    deletedlist.push(objSelectstatus.options[i].value);
                }
                postData['deleted'] = deletedlist;
            }
            //if (postData['cur_status'] != 'undone'){
            //    if (! document.getElementById("handle_user").value == ""){
            //        var userlist = [];
            //        var objSelectuser = document.upgradeform.handle_user; 
            //        for(var i = 0; i < objSelectuser.options.length; i++) { 
            //            if (objSelectuser.options[i].selected == true) {
            //                userlist.push(objSelectuser.options[i].value);
            //            }
            //        }
            //        postData['handle_user'] = userlist;
            //    }
            //}
            //console.log(postData)
            
            var act = '';
            if (postData['deleted'] == 'all' || postData['deleted'].length == 2){
                act = 'query_all';
            } else if (postData['deleted'].length == 1){
                if (postData['deleted'][0] == 0){
                    act = 'query_not_deleted';
                }else if (postData['deleted'][0] == 1){
                    act = 'query_deleted';
                }else {
                    act = 'null';
                }
            }

            var params = {
                url: '/upgrade/query_svn',
                method: 'post',
                singleSelect: false,
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 'postData': postData, 'act': act };
                },
            }
            $('#upgrade_op_table').bootstrapTable('refresh', params);
            return false;

        });
    },

    setHandleUser: function(){
        var objSelectstatus = document.upgradeform.cur_status_sel;
        var count = 0;
        for(var i = 0; i < objSelectstatus.options.length; i++) { 
            if (objSelectstatus.options[i].selected == true) 
            count = count + 1;
        }
        if (document.getElementById("cur_status_sel").value == "undone" && count == 1){
            $('#handle_user').prop('disabled', true);
            $('#handle_user').selectpicker('refresh');
            //$("#handle_user").selectpicker('setStyle', 'btn-warning');
        }else {
            $('#handle_user').prop('disabled', false);
            $('#handle_user').selectpicker('refresh');
            //$("#handle_user").removeAttr("disabled");
            //$("#handle_user").selectpicker('setStyle', 'btn-warning', 'remove');
            //$("#handle_user").selectpicker('setStyle', 'btn-default');
        }
    },

    selectpicker: function() {
        $('.selectpicker').selectpicker({
            style: 'btn-default',
            //width: "auto",
            size: 10,
            showSubtext:true,
        });
    },

    //数据校验
    operateCheck:function(arr){
        if (arr.length <= 0) {
            alert("请至少选择一行数据");
            return false;
        }
        if (arr.length > 1) {
            alert("只能编辑一行数据");
            return false;
        }
        return true;
    }
}