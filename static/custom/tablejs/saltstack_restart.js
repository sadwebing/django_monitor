$(".js-example-basic-multiple").select2({
    placeholder: "请选择要重启的服务"
});

$(function () {
    operate.operateInit();
});

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.GetProject();
        this.Getform();
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
                var html = "";
                $.each(data, function (index, item) { 
                    //循环获取数据 
                    var name = data[index];
                    html_name = "<option value='"+name+"'>"+name+"</option>";
                    html = html + html_name
                }); 
                $("#project").html(html);
                //for (var data in datas){
                //    $("#project").html("<option value='"+data+"'>"+data+"</option>");
                //}
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
            document.getElementById("commandform").reset();
            document.getElementById("project").reset();
            return false;
        });
    },

    Getform: function getEntity(commandform) {
        var formdata = {
            expr_form:document.getElementById("expr_form").value,
            target:document.getElementById("target").value,
            project:[],
        };
        var target = document.getElementById("target").value;
        if (formdata['expr_form'] == 'list'){
            formdata['target'] = target.replace(/[\s*]/g, '').split(',');
        }
        if (formdata['target'] == ''){
            $("#target").html("target 不能为空！");
        }
        var project = [];
        $("#project :selected").each(function(){
            project.push($(this).val())
        });
        formdata['project'] = project;
        return formdata;
    },
    
    Submit: function(){
        $("#btn_submit").bind('click',function () {
            var postData=operate.Getform();
            if (postData['project'].length == 0){
                alert("请至少选择一个服务进行重启！")
                return false;
            }
            //alert("获取到的表单数据为:"+JSON.stringify(postData));
            $.ajax({
                url: "/saltstack/command/restart",
                type: "post",
                contentType: 'application/json',
                data: JSON.stringify(postData),
                success: function (data, status) {
                    //alert(data);
                    var html = "";
                    data = JSON.parse(data)
                    //html = "<strong>"+postData['project']+"</strong>"
                    for (var project in data){
                        html = html + "<p><strong>"+project+"</strong></p><pre class='pre-scrollable'><xmp>"+data[project]+"</xmp></pre>";
                    }
                    $("#commandresults").html(html);
                    return false;
                },
                error:function(msg){
                    alert("目前只支持单台服务器进行操作，请检查minion ID！");
                    return false;
                }
            });
            return false;
        });
    },

};