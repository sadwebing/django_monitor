$(function () {
    operate.operateInit();
});

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.Getform();
        this.Submit();
        this.Results();
        this.GetProject();
        this.selectpicker();
        //this.showSelectedValue();
        this.Exe();
    },
    Getform: function getEntity(commandform) {
        var formdata = {
            expr_form:document.getElementById("expr_form").value,
            target:document.getElementById("target").value,
            function:document.getElementById("function").value,
            arguments:document.getElementById("arguments").value,
        };
        var target = document.getElementById("target").value;
        if (formdata['expr_form'] == 'list'){
            formdata['target'] = target.replace(/[\s*]/g, '').split(',');
        }
        if (formdata['target'] == ''){
            $("#target").html("target 不能为空！");
        }
        return formdata;
    },
    
    Reset: function (){
        $("#btn_reset").bind('click',function () {
            document.getElementById("commandform").reset();
            return false;
        });
    },

    Submit: function(){
        $("#btn_submit").bind('click',function () {
            var postData=operate.Getform();
            if (postData['target'] == ''){
                alert("Minion ID 不能为空！");
                return false;
            }
            if (postData['function'] != 'test.ping' &  postData['arguments'] == ''){
                alert("执行参数 不能为空！");
                return false;
            }
            //alert("获取到的表单数据为:"+JSON.stringify(postData));
            $.ajax({
                url: "/saltstack/command/execute",
                type: "post",
                contentType: 'application/json',
                dataType: "json",
                data: JSON.stringify(postData),
                success: function (data, status) {
                    //alert(data["zabbix.ag866.com"]);
                    var html = "";
                    var button = "";
                    for (var tgt in data){
                        //alert(tgt+data[tgt])
                        button = button + "<div class='btn-group'><button data-toggle='modal' data-target='#"+tgt+"' id='#"+tgt+"' type='button' class='btn btn-primary'>"+tgt+"</button></div><div class='modal fade' id='"+tgt+"' tabindex='-1' role='dialog' dialaria-labelledby='"+tgt+"'><div class='modal-dialog' role='document' style='width:1000px;'><div class='modal-content'><xmp>"+data[tgt]+"</xmp></div></div></div>";
                        //$("#" + tgt).modal({keyboard: true});
                        //button = button + "<button class='btn btn-primary' data-toggle='modal' data-target='#show_results'>"+tgt+"</button>"
                        html = html + "<p><strong>"+tgt+"</strong></p><pre class='pre-scrollable'><xmp>"+data[tgt]+"</xmp></pre>";
                    }
                    button = "<div class='btn-toolbar' role='toolbar'>" + button +"</div>" + "<hr>"
                    $("#commandresults").html(button+html);
                    for (var tgt in data){
                        $("#"+tgt).click(function(){
                            $(this).modal({keyboard: true});
                        });
                    }
                    return false;
                },
                error:function(msg){
                    alert("参数输入错误！");
                    return false;
                }
            });
            return false;
        });
    },

    Results: function(){
        $("#show_results").modal({
            keyboard: true
        })
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
            //width: "auto",
            size: 10,
            showSubtext:true,
        });
    },

    showSelectedValue: function (){
        var selectedValue = []; 
        var objSelect = document.projectreform.servers_id; 
        for(var i = 0; i < objSelect.options.length; i++) { 
            if (objSelect.options[i].selected == true) 
            selectedValue.push(objSelect.options[i].value);
        }
        return selectedValue;
    },

    Exe: function(){
        $("#btn_exe").bind('click',function () {
            //var postData=operate.Getform();
            var postData = {
                expr_form,
                target,
                function:document.getElementById("function2").value,
                arguments:document.getElementById("arguments2").value,
            };
            //console.log(postData)
            postData['target'] = operate.showSelectedValue();
            if (document.getElementById("project_active").value.length == 0){
                alert("请至少选择一个服务！")
                return false;
            }
            if (postData['target'].length == 0){
                alert("请至少选择一个服务器！")
                return false;
            }
            postData['expr_form'] = 'list';
            console.log(postData)
            //alert("获取到的表单数据为:"+JSON.stringify(postData));
            $.ajax({
                url: "/saltstack/command/execute",
                type: "post",
                contentType: 'application/json',
                dataType: "json",
                data: JSON.stringify(postData),
                success: function (data, status) {
                    var html = "";
                    var button = "";
                    for (var tgt in data){
                        button = button + "<div class='btn-group'><button data-toggle='modal' data-target='#"+tgt+"' id='#"+tgt+"' type='button' class='btn btn-primary'>"+tgt+"</button></div><div class='modal fade' id='"+tgt+"' tabindex='-1' role='dialog' dialaria-labelledby='"+tgt+"'><div class='modal-dialog' role='document' style='width:1000px;'><div class='modal-content'><xmp>"+data[tgt]+"</xmp></div></div></div>";
                        html = html + "<p><strong>"+tgt+"</strong></p><pre class='pre-scrollable'><xmp>"+data[tgt]+"</xmp></pre>";
                    }
                    button = "<div class='btn-toolbar' role='toolbar'>" + button +"</div>" + "<hr>"
                    $("#commandresults").html(button+html);
                    for (var tgt in data){
                        $("#"+tgt).click(function(){
                            $(this).modal({keyboard: true});
                        });
                    }
                    return false;
                },
                error:function(msg){
                    alert("参数输入错误！");
                    return false;
                }
            });
            return false;
        });
    },

};