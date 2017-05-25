
$('#upgrade_op_table').bootstrapTable({
    url: '/upgrade/query_svn',   //请求后台的URL（*） 
    method: 'post',      //请求方式（*） 
    toolbar: '#toolbar',    //工具按钮用哪个容器 
    striped: false,      //是否显示行间隔色 
    cache: false,      //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*） 
    pagination: true,     //是否显示分页（*） 
    //sortable: false,      //是否启用排序 
    sortOrder: "asc",     //排序方式 
    queryParams: function (params) {
        return { limit: params.limit, offset: params.offset, 'act':'query_all' };
    },//传递参数（*） 
    sidePagination: "server",   //分页方式：client客户端分页，server服务端分页（*） 
    pageNumber:1,      //初始化加载第一页，默认第一页 
    pageSize: 10,      //每页的记录行数（*） 
    pageList: [5, 10, 25, 50, 100, 'ALL'],  //可供选择的每页的行数（*） 
    search: true,      //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大 
    strictSearch: false, 
    showColumns: true,     //是否显示所有的列 
    showRefresh: true,     //是否显示刷新按钮 
    //showPaginationSwitch: true,
    //showFooter:true,
    minimumCountColumns: 2,    //最少允许的列数 
    clickToSelect: true,    //是否启用点击选中行 
    //height: 500,      //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度 
    uniqueId: "id",      //每一行的唯一标识，一般为主键列 
    showToggle:true,     //是否显示详细视图和列表视图的切换按钮 
    //cardView: true,     //是否显示详细视图 
    detailView: false,     //是否显示父子表 
    //height: getHeight(),
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
            field: 'id',
            title: '操作项',
            //align: 'center',
            width:'18%',
            events: operateEvents,
            formatter: this.operateFormatter,
            //width:300,
        },
    ]
});

    operateFormatter: function (value,row,index){
        return [
            '<a class="upgrade" href="javascript:void(0)" title="升级">',
            '<i class="glyphicon glyphicon-hand-up"> &ensp; </i>',
            '</a> ',
            '<a class="diff" href="javascript:void(0)" title="比对代码">',
            '<i class="glyphicon glyphicon-align-center"> &ensp; </i>',
            '</a>',
        ].join('');
        //if (row.cur_status == 'rollback'){
        //    content = content + [
        //    '<a class="rollback" href="javascript:void(0)" title="回退[禁用]" disabled="disabled">',
        //    '<i class="glyphicon glyphicon-hand-down"></i>',
        //    '</a>'
        //    ].join('');
        //}else {
        //    content = content + [
        //    '<a class="rollback" href="javascript:void(0)" title="回退">',
        //    '<i class="glyphicon glyphicon-hand-down"></i>',
        //    '</a>'
        //    ].join('');   
        //}

        //return content;
    },

    cur_statusFormatter: function (value,row,index) {
        var status = row.cur_status;
        if (status == 'undone'){
            content = '<span style="background-color: grey">未升级</span>';
            return content;
        }else if(status == 'done'){
            return "已升级";
        }else if(status == 'rollback'){
            content = '<span style="background-color: #FF6347">已回滚</span>';
            return content;
        }else {
            return "未定义";
        }
    },
};

window.operateEvents = {
    'click .upgrade': function (e, value, row, index) {
        console.log('click upgrade.')
        alert(row.project);
        return false;
    },
    'click .diff': function (e, value, row, index) {
        console.log('click diff.')
        alert(row.project);
        return false;
    },
    'click .rollback': function (e, value, row, index) {
        console.log('click rollback.')
        alert(row.project);
        return false;
    }
};  

