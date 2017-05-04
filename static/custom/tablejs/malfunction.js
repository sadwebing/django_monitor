$(function () {
    tableInit.Init_undone();
    operate.operateInit();
});

//初始化表格
var tableInit = {
    Init_undone: function () {
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: '/malfunction/Query',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            singleSelect:true,
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset };
            },//传递参数（*）
        });
        ko.applyBindings(this.myViewModel, document.getElementById("undone_table"));
    },
};

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.operateAdd();
        this.csoperateUpdate();
        this.saoperateUpdate();
        //this.operateSave();
        this.DepartmentModel = {
            id: ko.observable(),
            record_time: ko.observable(),
            mal_details: ko.observable(),
            record_user: ko.observable(),
            mal_reasons: ko.observable(),
            mal_status: ko.observable(),
            recovery_time: ko.observable(),
            time_all: ko.observable(),
            handle_user: ko.observable(),
        };
    },
    //新增
    operateAdd: function(){
        $('#btn_add').on("click", function () {
            $("#csAddModal").modal().on("shown.bs.modal", function () {
                var oEmptyModel = {
                    id: ko.observable(),
                    record_time: ko.observable(),
                    mal_details: ko.observable(),
                    record_user: ko.observable(),
                };
                ko.utils.extend(operate.DepartmentModel, oEmptyModel);
                ko.applyBindings(operate.DepartmentModel, document.getElementById("csAddModal"));
                operate.operatecsadd();
            }).on('hidden.bs.modal', function () {
                ko.cleanNode(document.getElementById("csAddModal"));
            });
        });
    },

    //编辑
    csoperateUpdate: function () {
        $('#btn_cs_edit').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            if (!operate.operateCheck(arrselectedData)) { return; }
            $("#csEditModal").modal().on("shown.bs.modal", function () {
                var arrselectedData = tableInit.myViewModel.getSelections();
                if (!operate.operateCheck(arrselectedData)) { return; }
                //将选中该行数据有数据Model通过Mapping组件转换为viewmodel
                ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData[0]));
                ko.applyBindings(operate.DepartmentModel, document.getElementById("csEditModal"));
                operate.operatecssubmit();
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("csEditModal"));
            });
        });
    },

    saoperateUpdate: function () {
        $('#btn_sa_edit').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            if (!operate.operateCheck(arrselectedData)) { return; }
            $("#saEditModal").modal().on("shown.bs.modal", function () {
                var arrselectedData = tableInit.myViewModel.getSelections();
                if (!operate.operateCheck(arrselectedData)) { return; }
                //将选中该行数据有数据Model通过Mapping组件转换为viewmodel
                ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData[0]));
                ko.applyBindings(operate.DepartmentModel, document.getElementById("saEditModal"));
                operate.operatesasubmit();
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("saEditModal"));
            });
        });
    },

    //保存数据
    operatecsadd: function () {
        $('#btn_cs_add').on("click", function () {
            //取到当前的viewmodel
            var oViewModel = operate.DepartmentModel;
            //将Viewmodel转换为数据model
            var oDataModel = ko.toJS(oViewModel);
            //console.log(oDataModel)
            var funcName = oDataModel.id?"Update":"Add";
            $.ajax({
                url: "/malfunction/"+funcName,
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

    operatecssubmit: function () {
        $('#btn_cs_submit').on("click", function () {
            //取到当前的viewmodel
            var oViewModel = operate.DepartmentModel;
            //将Viewmodel转换为数据model
            var oDataModel = ko.toJS(oViewModel);
            //console.log(oDataModel)
            var funcName = oDataModel.id?"Update":"Add";
            $.ajax({
                url: "/malfunction/"+funcName,
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

    operatesasubmit: function () {
        $('#btn_sa_submit').on("click", function () {
            //取到当前的viewmodel
            var oViewModel = operate.DepartmentModel;
            //将Viewmodel转换为数据model
            var oDataModel = ko.toJS(oViewModel);
            //alert(oDataModel.id)
            var funcName = oDataModel.id?"Update":"Add";
            $.ajax({
                url: "/malfunction/"+funcName,
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