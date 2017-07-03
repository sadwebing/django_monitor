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

    infoFormatter: function (value,row,index){
        var content = [
            '<a class="info text-info" href="javascript:void(0)" title="详情">',
                '详情',
            '</a>',
        ].join('');
        return content;
    },
};

window.infoEvents = {
    'click .info': function (e, value, row, index) {
        var html = row.info;
        var info_xmp = document.getElementById('info_xmp')
        info_xmp.innerHTML = html;
        $('#info_modal').modal('show');

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
