$(function () {
    tableInit.Init();
    operate.operateInit();
});

//全局变量
window.modal_results = document.getElementById("Checkresults");
window.modal_footer = document.getElementById("progressFooter");
window.modal_head = document.getElementById("progress_head");

//初始化表格
var tableInit = {
    Init: function () {
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: '/tomcat/tomcat_url/Query',         //请求后台的URL（*）
            method: 'post',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset, 'act':'query_all' };
            },//传递参数（*）
            columns: [
                {
                    checkbox: true,
                    width:'2%',
                },
                {
                    field: 'id',
                    title: 'id',
                    sortable: true,
                    width:'3%',
                    //align: 'center'
                },{
                    field: 'envir',
                    title: '环境',
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
                    field: 'minion_id',
                    title: 'Minion Id',
                    sortable: true,
                    //align: 'center',
                    width:'9%',
                },{
                    field: 'ip_addr',
                    title: 'Ip地址',
                    sortable: true,
                    //align: 'center',
                    width:'9%',
                },{
                    field: 'server_type',
                    title: '服务类型',
                    sortable: true,
                    width:'8%',
                    //align: 'center'
                },{
                    field: 'role',
                    title: '角色',
                    sortable: true,
                    width:'6%',
                    //align: 'center'
                }, {
                    field: 'domain',
                    title: '域名',
                    sortable: true,
                    width:'15%',
                    //align: 'center',
                    //events: this.cur_statusEvents,
                    formatter: this.cur_statusFormatter
                },{
                    field: 'url',
                    title: '检测地址',
                    sortable: true,
                    //align: 'center',
                    width:'18%',
                },{
                    field: 'status_',
                    title: '状态',
                    sortable: true,
                    width:'5%',
                    events: operateStatusEvents,
                    formatter: this.operateStatusFormatter,
                    //align: 'center'
                },{
                    field: 'info',
                    title: '备注',
                    sortable: true,
                    width:'auto',
                    //align: 'center'
                },{
                    field: 'operations',
                    title: '操作项',
                    //align: 'center',
                    width:'6%',
                    checkbox: false,
                    events: operateEvents,
                    formatter: this.operateFormatter,
                    //width:300,
                },
            ]

        });
        ko.applyBindings(this.myViewModel, document.getElementById("tomcat_table"));
    },

    operateStatusFormatter: function (value,row,index){
        if (row.status_ == 'active'){
            content = [
            '<div class="checkbox checkbox-slider--a" style="margin:0px;">',
                '<label>',
                    '<input type="checkbox" id='+ row.id +' class="update_status" checked><span></span>',
                '</label>',
            '</div>'
            ].join('');
        }else {
            content = [
            '<div class="checkbox checkbox-slider--a" style="margin:0px;">',
                '<label>',
                    '<input type="checkbox" id='+ row.id +' class="update_status"><span></span>',
                '</label>',
            '</div>'
            ].join('');
        }
        return content;
    },

    operateFormatter: function (value,row,index){
        content = [
        '<a class="check_server" href="javascript:void(0)" title="检测服务">',
        '<i class="text-primary"> 检测</i>',
        '</a>'
        ].join('');   
        return content;
    },
};

window.operateStatusEvents = {
    'click .update_status': function (e, value, row, index) {
        var postData = {
            id:row.id,
            status,
        };
        if (document.getElementById(row.id).checked){
            postData.status = 'active';
            //console.log(postData);
        }else {
            postData.status = 'inactive';
            //console.log(postData);
        }
        $.ajax({
            url: "/tomcat/tomcat_url/UpdateStatus",
            type: "post",
            data: JSON.stringify(postData),
            success: function (data, status) {
                toastr.success('状态更新成功！', row.project+": "+row.url);
                //ko.cleanNode(document.getElementById("tomcat_table"));
                row.status_ = postData.status;
                //alert(data);
                //tableInit.myViewModel.refresh();
            },
            error: function(msg){
                alert("失败，请检查日志！");
                tableInit.myViewModel.refresh();
            }
        });
        return false;
    },
};

window.operateEvents = {
    'click .check_server': function (e, value, row, index) {
        var postData = {
            minion_id:row.minion_id,
            server_type:row.server_type,
            domain:row.domain,
            url:row.url,
        };
        modal_results.innerHTML = "";
        modal_footer.innerHTML = "";
        $("#progress_bar").css("width", "30%");
        modal_head.style.color = 'blue';
        modal_head.innerHTML = "操作进行中，请勿刷新页面......";
        var socket = new WebSocket("ws://" + window.location.host + "/tomcat/tomcat_url/CheckServer");
        socket.onopen = function () {
            //console.log('WebSocket open');//成功连接上Websocket
            socket.send(JSON.stringify(postData));
        };
        $('#runprogress').modal('show');
        socket.onmessage = function (e) {
            data = eval('('+ e.data +')')
            //console.log('message: ' + data);//打印服务端返回的数据
            if (data.step == 'one'){
                $("#progress_bar").css("width", "50%");
                $('#Checkresults').append('<p> 项目名:&thinsp;<strong>' + row.project + '</strong></p>' );
                $('#Checkresults').append('<p> 服务器地址:&thinsp;<strong>' + row.minion_id + '</strong></p>' );
                $('#Checkresults').append('<p> 服务类型:&thinsp;<strong>' + row.server_type + '</strong></p>' );
                $('#Checkresults').append('<p> 角色:&thinsp;<strong>' + row.role + '</strong></p>' );
                $('#Checkresults').append('<p> 域名:&thinsp;<strong>' + row.domain + '</strong></p>' );
                $('#Checkresults').append('<p> 检测地址:&thinsp;<strong>' + row.url + '</strong></p>' );
                $('#Checkresults').append('<hr>' );
            }else if (data.step == 'final'){
                $("#progress_bar").css("width", "100%");
                modal_head.innerHTML = "检测完成！";
                $('#Checkresults').append('<p> 检测时间:&thinsp;<strong>' + data.access_time + '</strong></p>' );
                $('#Checkresults').append('<p> 检测状态:&thinsp;<strong>' + data.code + '</strong></p>' );
                $('#Checkresults').append('<p> 备注:&thinsp;<strong>' + data.info + '</strong></p>' );
                //console.log('websocket已关闭');
                modal_footer.innerHTML = '<button id="close_modal" type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span>关闭</button>'
            }
        }; 
        return false;
    },
}; 

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.selectpicker();
        this.operateAdd();
        this.operateUpdate();
        this.operateconfirmDelete();
        this.operateTomcatUrlSelect();
        //this.operateDelete();
        this.DepartmentModel = {
            id: ko.observable(),
            envir: ko.observable(),
            project: ko.observable(),
            minion_id: ko.observable(),
            ip_addr: ko.observable(),
            server_type: ko.observable(),
            role: ko.observable(),
            domain: ko.observable(),
            url: ko.observable(),
            status_: ko.observable(),
            info: ko.observable(),
        };
    },

    selectpicker: function docombjs() {
        $('.selectpicker').selectpicker({
            style: 'btn-default',
            //width: "auto",
            size: 15,
            showSubtext:true,
        });
    },

    operateTomcatUrlSelect: function(){
        $('#tomcat_url_active').on("click", function () {
            document.getElementById('tomcat_url_active').disabled = true;
            document.getElementById('tomcat_url_inactive').disabled = false;
            document.getElementById('tomcat_url_all').disabled = false;
            var params = {
                url: '/tomcat/tomcat_url/Query',
                method: 'post',
                singleSelect: false,
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 'act':'query_active' };
                },
            }
            tableInit.myViewModel.refresh(params);
        });
        $('#tomcat_url_inactive').on("click", function () {
            document.getElementById('tomcat_url_active').disabled = false;
            document.getElementById('tomcat_url_inactive').disabled = true;
            document.getElementById('tomcat_url_all').disabled = false;
            var params = {
                url: '/tomcat/tomcat_url/Query',
                method: 'post',
                singleSelect: false,                                                
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 'act':'query_inactive' };
                },
            }
            tableInit.myViewModel.refresh(params);
        });
        $('#tomcat_url_all').on("click", function () {
            document.getElementById('tomcat_url_active').disabled = false;
            document.getElementById('tomcat_url_inactive').disabled = false;
            document.getElementById('tomcat_url_all').disabled = true;
            var params = {
                url: '/tomcat/tomcat_url/Query',
                method: 'post',
                singleSelect: false,
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 'act':'query_all' };
                },
            }
            tableInit.myViewModel.refresh(params);
        });
    },

    //新增
    operateAdd: function(){
        $('#btn_add').on("click", function () {
            $("#myModal").modal().on("shown.bs.modal", function () {
                var oEmptyModel = {
                    envir: ko.observable(),
                    project: ko.observable(),
                    minion_id: ko.observable(),
                    ip_addr: ko.observable(),
                    server_type: ko.observable(),
                    role: ko.observable(),
                    domain: ko.observable(),
                    url: ko.observable(),
                    status_: ko.observable(),
                    info: ko.observable(),
                };
                ko.utils.extend(operate.DepartmentModel, oEmptyModel);
                ko.applyBindings(operate.DepartmentModel, document.getElementById("myModal"));
                operate.operateSave('Add');
            }).on('hidden.bs.modal', function () {
                ko.cleanNode(document.getElementById("myModal"));
            });
        });
    },

    //编辑
    operateUpdate: function () {
        $('#btn_edit').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            if (!operate.operateCheck(arrselectedData)) { return; }
            $("#myModal").modal().on("shown.bs.modal", function () {
                //operate.selectpicker();
                var arrselectedData = tableInit.myViewModel.getSelections();
                if (!operate.operateCheck(arrselectedData)) { return; }
                //将选中该行数据有数据Model通过Mapping组件转换为viewmodel
                ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData[0]));
                if (document.getElementById(operate.DepartmentModel.id()).checked){
                    operate.DepartmentModel.status_ = 'active';
                }else {
                    operate.DepartmentModel.status_ = 'inactive';
                }
                ko.applyBindings(operate.DepartmentModel, document.getElementById("myModal"));
                operate.operateSave('Update');
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("myModal"));
            });
        });
    },

    ViewModel: function() {
                var self = this;
                self.datas = ko.observableArray();
    },

    operateconfirmDelete: function () {
        $('#btn_confirm_delete').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            if (arrselectedData.length <= 0){
                alert("请至少选择一行数据");
                return false;
            }
            var vm = new operate.ViewModel();
            for (var i=0;i<arrselectedData.length;i++){
                //ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData[i]));
                //vm.datas.push(operate.DepartmentModel);
                vm.datas.push(ko.mapping.fromJS(arrselectedData[i]));
            }
            $("#confirmDeleteModal").modal().on("shown.bs.modal", function () {
                //ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData));
                //ko.applyBindings(operate.DepartmentModel, document.getElementById("confirmDeleteModal"));
                ko.applyBindings(vm, document.getElementById("confirmDeleteModal"));
                //datas = ko.mapping.fromJS(arrselectedData)
                var html = "";
                $.each(vm.datas(), function (index, item) { 
                    //循环获取数据
                    var name = vm.datas()[index];
                    //alert(name)
                    html_name = "<tr><td>"+name.id()+"</td><td>"+name.envir()+"</td><td>"+name.project()+"</td><td>"+name.minion_id()+"</td><td>"+name.ip_addr()+"</td><td>"+name.server_type()+"</td><td>"+name.role()+"</td><td>"+name.domain()+"</td><td>"+name.url()+"</td><td>"+name.status_()+"</td><td>"+name.info()+"</td></tr>";
                    html = html + html_name
                }); 
                $("#DeleteDatas").html(html);
                operate.operateDelete();
                //vm.datas.valueHasMutated();
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("confirmDeleteModal"));
            });
        });
    },

    //删除
    operateDelete: function () {
        $('#btn_delete').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            $.ajax({
                url: "/tomcat/tomcat_url/Delete",
                type: "post",
                contentType: 'application/json',
                data: JSON.stringify(arrselectedData),
                success: function (data, status) {
                    alert(data);
                    tableInit.myViewModel.refresh();
                },
                error:function(msg){
                    alert("失败，请检查日志！");
                    tableInit.myViewModel.refresh();
                }
            });
        });
    },
    //保存数据
    operateSave: function (funcName) {
        $('#btn_submit').on("click", function () {
            //取到当前的viewmodel
            var oViewModel = operate.DepartmentModel;
            console.log(oViewModel.project())
            if (! oViewModel.project()){
                alert('项目名 不能为空！')
                return false;
            }
            if (! oViewModel.minion_id()){
                alert('Minion Id 不能为空！')
                return false;
            }
            if (! oViewModel.ip_addr()){
                alert('Ip地址 不能为空！')
                return false;
            }
            if (! oViewModel.domain()){
                oViewModel.domain = 'null';
            }
            if (! oViewModel.info()){
                oViewModel.info = '';
            }
            if (! oViewModel.url()){
                oViewModel.url = 'null';
            }
            //将Viewmodel转换为数据model
            var oDataModel = ko.toJS(oViewModel);
            //var funcName = oDataModel.id?"Update":"Add";
            $.ajax({
                url: "/tomcat/tomcat_url/"+funcName,
                type: "post",
                data: oDataModel,
                success: function (data, status) {
                    alert(data);
                    tableInit.myViewModel.refresh();
                },
                error:function(msg){
                    alert("失败，请检查日志！");
                    tableInit.myViewModel.refresh();
                }
            });
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