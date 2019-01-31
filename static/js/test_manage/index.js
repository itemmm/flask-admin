layui.use(["jquery","layer","form"],function(){
    var $ = layui.jquery;
    var layer = layui.layer;
    var form = layui.form;

    $(document).on("click",".addParam",function(){
        let params = $("#params");
        let html = '<div class="layui-form-item">' +
            '                <div class="layui-inline">' +
            '                    <label class="layui-form-label">key</label>' +
            '                    <div class="layui-input-block">' +
            '                        <input type="text" name="key" autocomplete="off" class="layui-input">' +
            '                    </div>' +
            '                </div>' +
            '                <div class="layui-inline">' +
            '                    <label class="layui-form-label">value</label>' +
            '                    <div class="layui-input-inline">' +
            '                        <input type="text" name="value" autocomplete="off" class="layui-input">' +
            '                    </div>' +
            '                </div>' +
            '                <div class="layui-inline">' +
            '                    <button class="layui-btn layui-btn-primary layui-btn-sm addParam">增加</button><button class="layui-btn layui-btn-primary layui-btn-sm deleteParam">删除</button>' +
            '                </div>' +
            '            </div>';
        params.append(html);
    });

    $(document).on("click",".deleteParam",function(){
        let param = $(this).parent().parent();
        if($("#params").children("div.layui-form-item").length<=1){
            layer.alert('不可删除!', {icon: 5});
        }else{
            param.remove();
        }
    });


    function highLight(res){
        response = JSON.stringify(res.response,null,4);
        response = response.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>');
        return response.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match){
            let cls = 'number';
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                cls = 'key';
             } else {
                    cls = 'string';
                }
             } else if (/true|false/.test(match)) {
                cls = 'boolean';
             } else if (/null/.test(match)) {
                cls = 'null';
             }
             return '<span class="' + cls + '">' + match + '</span>';
        })
    }

    form.on("submit(test)",function(data){
        let field = data.field;
        let response = $("#response");
        let keys = [];
        $("input[name='key']").each(function(){
           keys.push($(this).val());
        });
        let values = [];
        $("input[name='value']").each(function(){
            values.push($(this).val());
        });
        let params = {"url":field.url,"method":field.method,"userAgent":field.userAgent,"keys":keys.join(","),"values":values.join(",")};
        $.ajax({
            type: "POST",
            url: "/testManage/test",
            data: params,
            success: function(res){
                if(res.code===0){
                    response.append(highLight(res));
                }else{
                    layer.alert(data.msg, {icon: 5});
                }
            },
            error: function(){
                layer.alert('操作失败，网络故障!', {icon: 5});
            }
        })
    });


    $(document).on("click",".addHeaders",function(){
        let headers = $("#headers");
        let addHeaders = $(".addHeaders");
        let html = '<div class="layui-form-item">' +
            '                    <label class="layui-form-label">user-agent</label>' +
            '                    <div class="layui-input-block">' +
            '                        <input type="text" name="userAgent" autocomplete="off" placeholder="请输入user-agent" class="layui-input" />' +
            '                    </div>' +
            '                </div>';
        addHeaders.addClass("deleteHeaders");
        addHeaders.text("删除headers");
        addHeaders.removeClass("addHeaders");
        headers.append(html);
        headers.removeClass("layui-hide");
    });

    $(document).on("click",".deleteHeaders",function(){
       let headers = $("#headers");
       let deleteHeaders = $(".deleteHeaders");
       deleteHeaders.addClass("addHeaders");
       deleteHeaders.text("添加headers");
       deleteHeaders.removeClass("deleteHeaders");
       headers.addClass("layui-hide");
       headers.children("div.layui-form-item").remove();
    });

});