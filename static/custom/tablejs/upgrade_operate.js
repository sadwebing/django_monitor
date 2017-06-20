$(function () {
    tableInit.Init();
    operate.operateInit();
});

var tableInit = {
    Init: function () {
        this.operateFormatter;
        this.cur_statusFormatter;
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: '/upgrade/query_svn',         //请求后台的URL（*）
            method: 'post',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset, 'act':'query_all' };
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
                    width:'3%',
                    //align: 'center'
                },{
                    field: 'svn_id',
                    title: '版本',
                    sortable: true,
                    width:'6%',
                    //align: 'center'
                }, {
                    field: 'id_time',
                    title: '版本时间',
                    sortable: true,
                    //align: 'center',
                    width:'9%',
                }, {
                    field: 'project',
                    title: '项目名',
                    sortable: true,
                    width:'18%',
                    //align: 'center'
                },{
                    field: 'cur_svn_id',
                    title: '当前版本',
                    sortable: true,
                    width:'6%',
                    //align: 'center'
                }, {
                    field: 'cur_status',
                    title: '状态',
                    sortable: true,
                    width:'6%',
                    //align: 'center',
                    //events: this.cur_statusEvents,
                    formatter: this.cur_statusFormatter
                },{
                    field: 'op_time',
                    title: '操作时间',
                    sortable: true,
                    //align: 'center',
                    width:'9%',
                },{
                    field: 'handle_user',
                    title: '操作人',
                    sortable: true,
                    width:'6%',
                    //align: 'center'
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

    operateFormatter: function (value,row,index){
        var content = [
            '<a class="upgrade text-info" href="javascript:void(0)" title="升级">',
                '升级',
            '</a>&ensp;',
            '<a class="diff text-primary" href="javascript:void(0)" title="比对代码">',
                '比对',
            '</a>&ensp;',
        ].join('');
        if (row.cur_status == 'rollback'){
        }else {
            content = content + [
            '<a class="rollback text-muted" href="javascript:void(0)" title="回退">',
                '回退',
            '</a>'
            ].join('');   
        }
        return content;
    },

    cur_statusFormatter: function (value,row,index) {
        var status = row.cur_status;
        if (status == 'undone'){
            content = '<span style="background-color: grey">未升级</span>';
            return content;
        }else if(status == 'done'){
            return "已升级";
        }else if(status == 'rollback'){
            content = '<span style="background-color: #FF6347">已回退</span>';
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
        socket.onmessage = function (e) {
            data = eval('('+ e.data +')')
            console.log('message: ' + data.message);//打印服务端返回的数据
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
    }
};  

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.operateUpgradeSelect();
        //this.setHandleUser();
        //this.selectpicker();
    },

    operateUpgradeSelect: function(){
        $('#btn_op_search').on("click", function () {
            var postData = {
                project:"all",
                cur_status:"all",
                handle_user:"all",
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
            if (document.getElementById("cur_status").value != ""){
                var statuslist = [];
                var objSelectstatus = document.upgradeform.cur_status; 
                for(var i = 0; i < objSelectstatus.options.length; i++) { 
                    if (objSelectstatus.options[i].selected == true) 
                    statuslist.push(objSelectstatus.options[i].value);
                }
                postData['cur_status'] = statuslist;
            }
            if (postData['cur_status'] != 'undone'){
                if (! document.getElementById("handle_user").value == ""){
                    var userlist = [];
                    var objSelectuser = document.upgradeform.handle_user; 
                    for(var i = 0; i < objSelectuser.options.length; i++) { 
                        if (objSelectuser.options[i].selected == true) {
                            userlist.push(objSelectuser.options[i].value);
                        }
                    }
                    postData['handle_user'] = userlist;
                }
            }
            console.log(postData)
            return false;
            //var params = {
            //    url: '/tomcat/tomcat_url/Query',
            //    method: 'post',
            //    singleSelect: false,
            //    queryParams: function (param) {
            //        return { limit: param.limit, offset: param.offset, 'act':'query_active' };
            //    },
            //}
            //tableInit.myViewModel.refresh(params);

        });
    },

    setHandleUser: function(){
        var objSelectstatus = document.upgradeform.cur_status;
        var count = 0;
        for(var i = 0; i < objSelectstatus.options.length; i++) { 
            if (objSelectstatus.options[i].selected == true) 
            count = count + 1;
        }
        if (document.getElementById("cur_status").value == "undone" && count == 1){
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