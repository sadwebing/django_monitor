$(function () {
    tableInit.Init();
    //operate.operateInit();
});

//初始化表格
var tableInit = {
    Init: function () {
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: '/upgrade/op_history/Query',         //请求后台的URL（*）
            method: 'post',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            //singleSelect:true,
            clickToSelect: false,
            queryParams: function (param) {
                return { limit: 1000, offset: param.offset, 'act':'query_all', };
            },//传递参数（*）
        });
        ko.applyBindings(this.myViewModel, document.getElementById("upgrade_op_history"));
    },
};
