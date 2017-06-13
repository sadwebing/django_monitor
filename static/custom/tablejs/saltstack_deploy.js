$(function () {
    operate.operateInit();
});

//全局变量
window.modal_results = document.getElementById("OperateDeployresults");
window.modal_footer = document.getElementById("progressFooter");
window.modal_head = document.getElementById("progress_head");

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.selectpicker();
        this.GetProject();
        this.CheckMinion();
        this.SubmitDeploy();

        $('#btn_clear').bind('click', function(){
           document.getElementById('deploy_results').innerHTML = "";
        });
    },

    getNowFormatDate: function (type) {
        var seperator1 = "-";
        var seperator2 = ":";
        var dtCur = new Date();
        var yearCur = dtCur.getFullYear();
        var monCur = dtCur.getMonth() + 1;
        var dayCur = dtCur.getDate();
        var hCur = dtCur.getHours();
        var mCur = dtCur.getMinutes();
        var sCur = dtCur.getSeconds();
        var currentdate = yearCur + seperator1 + (monCur < 10 ? "0" + monCur : monCur) + seperator1 + (dayCur < 10 ? "0" + dayCur : dayCur) + " " + (hCur < 10 ? "0" + hCur : hCur) + seperator2 + (mCur < 10 ? "0" + mCur : mCur) + seperator2 + (sCur < 10 ? "0" + sCur : sCur);
        var timestamp = yearCur + (monCur < 10 ? "0" + monCur : monCur) + (dayCur < 10 ? "0" + dayCur : dayCur) + (hCur < 10 ? "0" + hCur : hCur) + (mCur < 10 ? "0" + mCur : mCur) + (sCur < 10 ? "0" + sCur : sCur);
        if (type == 'normal'){
            return currentdate;
        }else if (type = 'timestamp'){
            return timestamp;
        }
        
    } ,

    GetModuleName: function (radio_name){
        var obj = document.getElementsByName(radio_name);
        for(i=0;i<obj.length;i++) { 
            if(obj[i].checked) { 
                return obj[i].value; 
            } 
        }
        return "undefined";
    },

    DisplayProjectActive: function () {
            var module = operate.GetModuleName('deploy_module');
            var DisplaySel = document.getElementById('tomcat_projects');
            //console.log(project);
            if (module == 'tomcat') {
                //console.log(module + ": true")
                DisplaySel.style.display = "inline";
            }else {
                //console.log(module + ": false")
                DisplaySel.style.display = "none";
            }
    },

    GetMinionId: function (){
        var value = document.getElementById('minion_id').value;
        if (value){
            return value.replace(/[\s*]/g, '').split(',');
        }else {
            return false;
        }
    },

    CheckMinion: function () {
        $('#check_minion').bind('click',function () {
            var curTime = operate.getNowFormatDate();
            var minion_id = operate.GetMinionId();
            if (! minion_id){
                alert("Minion id 不能为空！");
                return false;
            }
            //console.log(minion_id)
            var socket = new WebSocket("ws://" + window.location.host + "/saltstack/check_minion");
            socket.onopen = function () {
                //console.log('WebSocket open');//成功连接上Websocket
                socket.send(JSON.stringify(minion_id));//发送数据到服务端
            };
            socket.onmessage = function (e) {
                data = eval('('+ e.data +')')
                //console.log('message: ' + data);//打印服务端返回的数据
                $('#deploy_results').append('<p>'+ operate.getNowFormatDate('normal') +' '+ data.minion_id +': '+ data.test_ping +'<p>');
            }; 
            return false;
        });
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

    showSelectedValue: function (){
        var selectedValue = []; 
        var objSelect = document.getElementById('project_active'); 
        for(var i = 0; i < objSelect.options.length; i++) { 
            if (objSelect.options[i].selected == true) 
            selectedValue.push(objSelect.options[i].value);
        }
        return selectedValue;
    },

    SubmitDeploy: function(){
        $("#btn_submit_deploy").bind('click',function () {
            var minion_id = operate.GetMinionId();
            if (! minion_id){
                alert("Minion id 不能为空！");
                return false;
            }
            var module = operate.GetModuleName('deploy_module');
            var project = document.getElementById('project_active').value;
            if (module == 'tomcat' && project == "") {
                alert("请选择要部署的Tomcat！")
                return false;
            }
            var postData = {
                minion_id:minion_id,
                module:module,
                project:project,
            }
            //console.log(minion_id +": "+ module +" "+ project)
            //console.log(minion_id.length)
            //return false;
            modal_results.innerHTML = "";
            modal_footer.innerHTML = "";
            $("#progress_bar").css("width", "30%");
            modal_head.style.color = 'blue';
            modal_head.innerHTML = "操作进行中，请勿刷新页面......";
            var socket = new WebSocket("ws://" + window.location.host + "/saltstack/deploy/deploy");
            socket.onopen = function () {
                //console.log('WebSocket open');//成功连接上Websocket
                //socket.send($('#message').val());//发送数据到服务端
                socket.send(JSON.stringify(postData))
            };
            $('#runprogress').modal('show');
            $('#deploy_results').append('<p>模块: '+ postData.module +'<p>');
            socket.onmessage = function (e) {
                //return false;
                data = eval('('+ e.data +')')
                //console.log('message: ' + data);//打印服务端返回的数据
                if (data.step == 'one'){
                    $("#progress_bar").css("width", "50%");
                    modal_head.innerHTML = "连接成功，部署中......";
                }else if (data.step == 'final'){
                    var button = ""
                    var button_html = "";
                    var width = 50*data.minion_count/data.minion_all + 50
                    if (data.result == ""){
                        $('#OperateDeployresults').append('<p>Minion ID: '+ data.minion_id +'</p>');
                        $('#OperateDeployresults').append('<p>模块: '+ data.module +'</p>');
                        if (! data.project == ""){
                            $('#OperateDeployresults').append('<p>项目: '+ data.project +'</p>');
                        }
                        $('#OperateDeployresults').append('<p>部署中......</p>');
                    }else {
                        var timestamp = operate.getNowFormatDate('timestamp')
                        $("#progress_bar").css("width", width+"%");
                        modal_head.innerHTML = "总共："+ data.minion_all +" 已完成："+ data.minion_count;
                        $('#OperateDeployresults').append('<p>部署完成......</p>');
                        if (data.result == 'not return'){
                            button = [                        
                            '<div class="btn-group" style="width:18%; margin-bottom:5px; margin-right:10px;">',
                                '<button data-toggle="modal" data-target="#'+data.minion_id+'_'+timestamp+'" id="#'+data.minion_id+'_'+timestamp+'" type="button" class="btn btn-danger" style="width:100%;">'+data.minion_id+'',
                                '</button>',
                            '</div>',].join("");
                        }else {
                            button = [                        
                            '<div class="btn-group" style="width:18%; margin-bottom:5px; margin-right:10px;">',
                                '<button data-toggle="modal" data-target="#'+data.minion_id+'_'+timestamp+'" id="#'+data.minion_id+'_'+timestamp+'" type="button" class="btn btn-info" style="width:100%;">'+data.minion_id+'',
                                '</button>',
                            '</div>',].join("");
                        }

                        button_html = button_html + button + [
                            '<div class="modal fade" id="'+data.minion_id+'_'+timestamp+'" tabindex="-1" role="dialog" dialaria-labelledby="'+data.minion_id+'_'+timestamp+'" aria-hidden="true">',
                                '<div class="modal-dialog" style="width:1000px;">',
                                    '<div class="modal-content" >',
                                        '<div class="modal-body">',
                                            '<xmp>'+data.result+'</xmp>',
                                        '</div>',
                                    '</div>',
                                '</div>',
                            '</div>',].join("");
                        $('#deploy_results').append(button_html);
                    }
                    if (data.minion_count == data.minion_all){
                        modal_footer.innerHTML = '<button id="close_modal" type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span>关闭</button>'
                    }
                }
            }; 

            return false;
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
};