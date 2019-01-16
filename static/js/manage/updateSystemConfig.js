layui.use(["layer","form","jquery"],function(){
    var layer = layui.layer;
    var form = layui.form;
    var $ = layui.jquery;


    form.on("submit(save)",function(data){
        let params = data.field;
        $.ajax({
            type:"POST",
            url: "/business/updateSystemConfig",
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