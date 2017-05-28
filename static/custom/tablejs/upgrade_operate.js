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
                    width:'18%',
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
            '<a class="upgrade" href="javascript:void(0)" title="升级">',
            '<i class="text-primary"> 升级</i>',
            '</a> &ensp; ',
            '<a class="diff" href="javascript:void(0)" title="比对代码">',
            '<i class="text-primary"> 比对</i>',
            '</a>&ensp; ',
        ].join('');
        if (row.cur_status == 'rollback'){
        }else {
            content = content + [
            '<a class="rollback" href="javascript:void(0)" title="回退">',
            '<i class="text-primary"> 回退</i>',
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
        console.log('click upgrade. '+row.project+" "+row.cur_status)
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
        this.GetProject();
    },

    operateUpgradeSelect: function(){
        $('#btn_op_search').on("click", function () {
            var postData = {
                project:"all",
                cur_status:document.getElementById("cur_status").value,
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
        if (document.getElementById("cur_status").value == "undone"){
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

    GetProject: function(){
        $.ajax({
            url: "/saltstack/restart/get_project",
            type: "post",
            contentType: 'application/json',
            //data: JSON.stringify(postData),
            success: function (datas, status) {
                //alert(datas);
                var data = eval(datas);
                //var html = "<option value=''></option>";
                var html_B79 = "";
                var html_P02 = "";
                var html_E02 = "";
                var html_NWF = "";
                var html_PUBLIC = "";
                $.each(data, function (index, item) { 
                    //循环获取数据 
                    var name = data[index];
                    //console.log(data)
                    //html_name = "<option>"+name+"</option>";
                    if (name.product === 'B79') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_B79 = html_B79 + html_name
                    }else if (name.product === 'P02') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_P02 = html_P02 + html_name
                    }else if (name.product === 'E02') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_E02 = html_E02 + html_name
                    }else if (name.product === 'NWF') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_NWF = html_NWF + html_name
                    }else if (name.product === 'PUBLIC') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_PUBLIC = html_PUBLIC + html_name
                    }
                }); 
                //$("#project").html(html);
                //$("#project_active").html(html);
                var html = "<optgroup label='B79'>" + html_B79 + "</optgroup>" + "<optgroup label='P02'>" + html_P02 + "</optgroup>" + "<optgroup label='E02'>" + html_E02 + "</optgroup>" + "<optgroup label='NWF'>" + html_NWF + "</optgroup>" + "<optgroup label='PUBLIC'>" + html_PUBLIC + "</optgroup>"
                var html_cur_status = [
                    '<option value="all">所有</option>' ,
                    '<option value="undone">未升级</option> ',
                    '<option value="done">已升级</option> ',
                    '<option value="rollback">已回滚</option>',
                ].join('');
                document.getElementById('project_active').innerHTML=html;
                document.getElementById('cur_status').innerHTML=html_cur_status;
                $('.selectpicker').selectpicker('refresh');
                return false;
            },
            error:function(msg){
                alert("获取项目失败！");
                return false;
            }
        });
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