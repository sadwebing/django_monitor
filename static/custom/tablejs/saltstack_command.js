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

};