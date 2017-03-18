$(function () {
    operate.operateInit();
});

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.Getform();
        this.Submit();
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
    
    Submit: function(){
        $("#btn_submit").bind('click',function () {
            var postData=operate.Getform();
            //alert("获取到的表单数据为:"+JSON.stringify(postData));
            $.ajax({
                url: "/saltstack/command/execute",
                type: "post",
                contentType: 'application/json',
                data: JSON.stringify(postData),
                success: function (data, status) {
                    //alert(data);
                    var html = "";
                    data = JSON.parse(data);
                    if (postData['function'] == 'test.ping' || postData['function'] == 'cmd.run'){
                        for (var tgt in data){
                            html = html + "<p><strong>"+tgt+"</strong></p><pre>"+data[tgt]+"</pre>";
                        }
                    }else {
                        for (var tgt in data){
                            //alert(data[tgt])
                            html = html + "<p><strong>"+tgt+"</strong></p><pre>"+data[tgt]+"</pre>";
                        }
                    }
                    $("#commandresults").html(html);
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