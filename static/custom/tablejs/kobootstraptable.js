//添加ko自定义绑定
ko.bindingHandlers.myBootstrapTable = {
    init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
        //这里的oParam就是绑定的viewmodel
        var oViewModel = valueAccessor();
        var $ele = $(element).bootstrapTable(oViewModel.params);
        //给viewmodel添加bootstrapTable方法
        oViewModel.bootstrapTable = function () {
            return $ele.bootstrapTable.apply($ele, arguments);
        }
    },
    update: function (element, valueAccessor, allBindingsAccessor, viewModel) {}
};

//初始化
(function ($) {
    //向ko里面新增一个bootstrapTableViewModel方法
    ko.bootstrapTableViewModel = function (options) {
        var that = this;

        this.default = {
            striped: true,
            cache: false,
            pagination: true,
            sortable: false,
            pageNumber: 1,
            pageSize: 10,
            pageList: [10, 25, 50, 100, 'ALL'],
            search: true,
            uniqueId: "id",
            showColumns: true,
            showRefresh: true,
            minimumCountColumns: 2,
            clickToSelect: true,
            showToggle: true,
            cardView: false,
            detailView: false,
        };
        this.params = $.extend({}, this.default, options || {});

        //得到选中的记录
        this.getSelections = function () {
            var arrRes = that.bootstrapTable("getSelections")
            return arrRes;
        };

        //刷新
        this.refresh = function () {
            that.bootstrapTable("refresh");
        };
    };
})(jQuery);

$(function () {
    $("#reset").bind('click',function () {
        function clearInputFile(f){
            if(f.value){
                try{
                    f.value = ''; //for IE11, latest Chrome/Firefox/Opera...
                }catch(err){
                }
                if(f.value){ //for IE5 ~ IE10
                    var form = document.createElement('form'), ref = f.nextSibling, p = f.parentNode;
                    form.appendChild(f);
                    form.reset();
                    p.insertBefore(f,ref);
                }
            }
        }
    });
});

$(function (){
    $(".form_datetime").datetimepicker({
        format: "yyyy-mm-dd hh:ii",
        autoclose: true,
        todayBtn: true,
        language:'zh-CN',
        minView: 0,
        maxView: 1,
        todayHighlight: 1,
        pickerPosition:"bottom-right"
    });
});