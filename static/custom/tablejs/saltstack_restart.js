//$(".js-example-basic-multiple").select2({
//    placeholder: "请选择要重启的服务"
//});
//$(".js-example-basic-single").select2({
//    placeholder: "请选择要重启的服务"
//});

$(function () {
    operate.operateInit();
});

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.GetProject();
        //this.GetProjectServers();
        this.selectpicker();
        //this.Getprojectreform();
        this.Submit();
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
                document.getElementById('project_active').innerHTML=html;
                $('.selectpicker').selectpicker('refresh');
                return false;
            },
            error:function(msg){
                alert("获取项目失败！");
                return false;
            }
        });
    },

    Reset: function (){
        $("#btn_reset").bind('click',function () {
            document.getElementById("projectreform").reset();
            document.getElementById("target").reset();
            return false;
        });
    },
    GetProjectServers: function(){
        var projectlist = []
        //var project = document.getElementById("project_active").value;
        var objSelectproject = document.projectreform.project_active; 
        for(var i = 0; i < objSelectproject.options.length; i++) { 
            if (objSelectproject.options[i].selected == true) 
            projectlist.push(objSelectproject.options[i].value);
        }
        console.log(projectlist);
        var postData = {};
        postData['project'] = projectlist;
        $.ajax({
            url: "/saltstack/restart/get_project_servers",
            type: "post",
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(postData),
            success: function (datas, status) {
                //alert(datas);
                var data = eval(datas);
                //var html = "<option value=''></option>";
                var html = "";
                for (var project in data){
                    html_tmp = "";
                    $.each(data[project], function (index, item) { 
                        //循环获取数据 
                        var name = data[project][index];
                        //html_name = "<option>"+name+"</option>";
                        console.log(name.role)
                        if (name.status === 'inactive') {
                            html_name = "<option value='"+name.server_ip+"' data-subtext='"+name.info+" "+name.role+"' disabled>"+name. server_ip+"</option>";
                        }else {
                            html_name = "<option value='"+name.server_ip+"' data-subtext='"+name.info+" "+name.role+"'>"+name.server_ip+"</ option>";
                        }
                        html_tmp = html_tmp + html_name
                    }); 
                    html_tmp = "<optgroup label='"+ project +"'>" + html_tmp + "</optgroup>";
                    html = html + html_tmp;
                }
                document.getElementById('servers_id').innerHTML=html;
                //$('.selectpicker').selectpicker({title:"请选择服务器地址"});
                $('.selectpicker').selectpicker('refresh');
                return false;
            },
            error:function(msg){
                alert("获取项目服务器地址失败！");
                return false;
            }
        });
    },

    selectpicker: function() {
        $('.selectpicker').selectpicker({
            style: 'btn-default',
            width: "auto",
            size: 10,
            showSubtext:true,
        });
    },
    
    //Getform: function getEntity(commandform) {
    //    var formdata = {
    //        expr_form:document.getElementById("expr_form").value,
    //        target:document.getElementById("target").value,
    //        project:[],
    //    };
    //    var target = document.getElementById("target").value;
    //    if (formdata['expr_form'] == 'list'){
    //        formdata['target'] = target.replace(/[\s*]/g, '').split(',');
    //    }
    //    if (formdata['target'] == ''){
    //        $("#target").html("target 不能为空！");
    //    }
    //    var project = [];
    //    $("#project :selected").each(function(){
    //        project.push($(this).val())
    //    });
    //    formdata['project'] = project;
    //    return formdata;
    //},

    //Getprojectreform: function getEntity(projectreform) {
    //    var formdata = {
    //        project:document.getElementById("project_active").value,
    //        server_id:document.getElementById("servers_id").value,
    //    };
    //    if (formdata['project'] == ''){
    //        alert("项目名 不能为空！");
    //    }
    //    if (formdata['server_id'] == ''){
    //        alert("服务器地址 不能为空！");
    //    }
    //    return formdata;
    //},
    
    Submit: function(){
        var modal_results = document.getElementById("OperateRestartresults");
        var modal_footer = document.getElementById("progressFooter");
        var modal_head = document.getElementById("progress_head");
        $("#btn_submit").bind('click',function () {
            //var postData=operate.Getform();
            var postData = {
                project:document.getElementById("project_active").value,
                server_id:document.getElementById("servers_id").value,
            };
            if (postData['project'].length == 0){
                alert("请至少选择一个服务进行重启！")
                return false;
            }
            if (postData['server_id'].length == 0){
                alert("请至少选择一个服务器进行重启！")
                return false;
            }
            //alert("获取到的表单数据为:"+JSON.stringify(postData));
            modal_results.innerHTML = "";
            modal_footer.innerHTML = "";
            $("#progress_bar").css("width", "30%");
            modal_head.innerHTML = "操作进行中，请勿刷新页面......";
            var socket = new WebSocket("ws://" + window.location.host + "/saltstack/command/restart");
            socket.onopen = function () {
                console.log('WebSocket open');//成功连接上Websocket
                //socket.send($('#message').val());//发送数据到服务端
                socket.send(JSON.stringify(postData))
            };
            $('#runprogress').modal('show');
            socket.onmessage = function (e) {
                //return false;
                data = eval('('+ e.data +')')
                console.log('message: ' + data);//打印服务端返回的数据
                if (data.step == 'one'){
                    $("#progress_bar").css("width", "50%");
                    $('#OperateRestartresults').append('<p>' + data['project'] + ':&thinsp;<strong>' + data['server_id'] + '</strong></p>' );
                }else if (data.step == 'final'){
                    modal_head.innerHTML = "服务重启完成...";
                    $("#progress_bar").css("width", "100%");
                    $('#OperateRestartresults').append('<pre>' + data['result'] + '</pre>');
                    console.log('websocket已关闭');
                    modal_footer.innerHTML = '<button id="close_modal" type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span>关闭</button>'
                }
            }; 

            return false;
        });
        $("#btn_submit").bind('click',function () {
            $("#progress_bar").css("width", "30%");
            modal_head.innerHTML = "操作进行中，请勿刷新页面......";
        });
        $("#restart_panel").bind('click',function () {
            that = document.getElementById("projectreform")
            if (that.style.display == "none"){
                that.style.display = "inline";
                document.getElementById('restart_panel').innerHTML = "-";
                document.getElementById('restart_panel').title = "隐藏";
            }else {
                that.style.display = "none";
                document.getElementById('restart_panel').innerHTML = "+";
                document.getElementById('restart_panel').title = "展开";
            }
        });
    },

};