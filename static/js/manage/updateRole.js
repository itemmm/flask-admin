layui.use(["form","jquery","element"],function(){
    var form = layui.form;
    var $ = layui.jquery;
    var element = layui.element;




    form.on("submit(save)",function(data){
        let ids = null;
        $("input[name='resource']:checkbox").each(function () {
            if ($(this).prop("checked")) {
                if (ids == null) {
                    ids = $(this).val();
                } else {
                    ids += ',' + $(this).val();
                }
            }
        });
        let params = {"roleId":data.field.roleId,"roleDes":data.field.roleDes,"resource":ids};
        $.ajax({
            type: "POST",
            url: "/business/updateRole",
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