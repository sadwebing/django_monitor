$(function () {
    tableInit.Init();
    operate.operateInit();
});

//初始化表格
var tableInit = {
    Init: function () {
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: '/tomcat/tomcat_project',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset };
            },//传递参数（*）
        });
        ko.applyBindings(this.myViewModel, document.getElementById("project_table"));
    }
};

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.operateAdd();
        this.operateUpdate();
        this.operateDelete();
        this.DepartmentModel = {
            id: ko.observable(),
            product: ko.observable(),
            project: ko.observable(),
            code_dir: ko.observable(),
            tomcat: ko.observable(),
            main_port: ko.observable(),
            jdk: ko.observable(),
            script: ko.observable(),
            status_: ko.observable(),
        };
    },
    //新增
    operateAdd: function(){
        $('#btn_add').on("click", function () {
            $("#mytomcatproductModal").modal().on("shown.bs.modal", function () {
                var oEmptyModel = {
                   id: ko.observable(),
                   product: ko.observable(),
                   project: ko.observable(),
                   code_dir: ko.observable(),
                   tomcat: ko.observable(),
                   main_port: ko.observable(),
                   jdk: ko.observable(),
                   script: ko.observable(),
                   status_: ko.observable(),
                };
                ko.utils.extend(operate.DepartmentModel, oEmptyModel);
                ko.applyBindings(operate.DepartmentModel, document.getElementById("mytomcatproductModal"));
                operate.operateSave();
            }).on('hidden.bs.modal', function () {
                ko.cleanNode(document.getElementById("mytomcatproductModal"));
            });
        });
    },
    //编辑
    operateUpdate: function () {
        $('#btn_edit').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            if (!operate.operateCheck(arrselectedData)) { return; }
            $("#mytomcatproductModal").modal().on("shown.bs.modal", function () {
                var arrselectedData = tableInit.myViewModel.getSelections();
                if (!operate.operateCheck(arrselectedData)) { return; }
                //将选中该行数据有数据Model通过Mapping组件转换为viewmodel
                ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData[0]));
                ko.applyBindings(operate.DepartmentModel, document.getElementById("mytomcatproductModal"));
                operate.operateSave();
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("mytomcatproductModal"));
            });
        });
    },
    //删除
    operateDelete: function () {
        $('#btn_delete').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            $.ajax({
                url: "/tomcat/Delete",
                type: "post",
                contentType: 'application/json',
                data: JSON.stringify(arrselectedData),
                success: function (data, status) {
                    alert(status);
                    //tableInit.myViewModel.refresh();
                }
            });
        });
    },
    //保存数据
    operateSave: function () {
        $('#btn_submit').on("click", function () {
            //取到当前的viewmodel
            var oViewModel = operate.DepartmentModel;
            //将Viewmodel转换为数据model
            var oDataModel = ko.toJS(oViewModel);var funcName = oDataModel.id?"Update":"Add";
            $.ajax({
                url: "/tomcat/"+funcName,
                type: "post",
                data: oDataModel,
                success: function (data, status) {
                    alert(status);
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