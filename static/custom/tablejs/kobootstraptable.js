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
            sortable: true,
            sortOrder: "asc",
            pageNumber: 1,
            pageSize: 10,
            pageList: [5, 10, 25, 50, 100, 'ALL'],
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
        this.refresh = function (params) {
            if (params){
                that.bootstrapTable("refresh", params);
            }else {that.bootstrapTable("refresh");}
        };
        this.destroy = function () {
            that.bootstrapTable("destroy");
        };
        this.getOptions = function () {
            var arrRes = that.bootstrapTable("getOptions");
            return arrRes;
        };
        this.removeAll = function () {
            that.bootstrapTable("removeAll");
        };
        this.refreshOptions = function () {
            that.bootstrapTable("refreshOptions");
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




$(function (){
    function GetDateDiff(startTime, endTime, diffType) {
        //将xxxx-xx-xx的时间格式，转换为 xxxx/xx/xx的格式
        startTime = startTime.replace(/\-/g, "/");
        endTime = endTime.replace(/\-/g, "/");
    
        //将计算间隔类性字符转换为小写
        diffType = diffType.toLowerCase();
        var sTime =new Date(startTime); //开始时间
        var eTime =new Date(endTime); //结束时间
        //作为除数的数字
        var divNum =1;
        switch (diffType) {
            case"second":
                divNum =1000;
            break;
            case"minute":
                divNum =1000*60;
            break;
            case"hour":
                divNum =1000*3600;
            break;
            case"day":
                divNum =1000*3600*24;
            break;
                default:
            break;
        }
    return parseInt((eTime.getTime() - sTime.getTime()) / parseInt(divNum));
    }

});