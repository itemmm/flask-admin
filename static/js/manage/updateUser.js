layui.use(["form","jquery","element"],function() {
    var form = layui.form;
    var $ = layui.jquery;
    var element = layui.element;

    form.on("submit(save)",function(data){
        let extraResourceList = null;
        let forbiddenResourceList = null;
        $("input[name='extraResource']:checkbox").each(function () {
            if ($(this).prop("checked")) {
                if (extraResourceList == null) {
                    extraResourceList = $(this).val();
                } else {
                    extraResourceList += ',' + $(this).val();
                }
            }
        });
        $("input[name='forbiddenResource']:checkbox").each(function () {
            if ($(this).prop("checked")) {
                if (forbiddenResourceList == null) {
                    forbiddenResourceList = $(this).val();
                } else {
                    forbiddenResourceList += ',' + $(this).val();
                }
            }
        });
        let params = {
            "userId":data.field.userId,
            "loginName":data.field.loginName,
            "nickName":data.field.nickName,
            "roleId":data.field.role,
            "extraResourceList":extraResourceList,
            "forbiddenResourceList":forbiddenResourceList};
        $.ajax({
            type: "POST",
            url: "/business/updateUser",
            data: params,
            success: function(res){
                if(res.code===0){
                    layer.alert(res.msg, {icon: 6}, function () {
                        let index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                        parent.layer.close(index); //再执行关闭
                    });
                } else{
                    layer.alert(res.msg, {icon: 5});
                }
            },
            error:function(){
                layer.alert('操作失败，网络故障!', {icon: 5});
            }
        })
    })

});