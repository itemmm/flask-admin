layui.use(["element","jquery","layer","form"],function(){
    var element = layui.element;
    var $ = layui.jquery;
    var layer = layui.layer;
    var form = layui.form;


    $.ajax({
        type: "POST",
        url: "/business/getRole",
        success: function(res){
            for(i=0;i<res.data.length;i++){
                let html = '<option value="'+res.data[i].roleId+'">'+res.data[i].roleName+'</option>';
                $("#role").append(html);
            }
            form.render();
        }
    });

    form.on("submit(save)",function (data) {
        let params = data.field;
        $.ajax({
            type: "POST",
            url: "",
            data: {"loginName":params.loginName,"nickName":params.nickName,"role":params.role},
            success: function (res) {
                if(res.code === 0){
                    layer.alert(res.msg, {icon: 6}, function () {
                        let index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                        parent.layer.close(index); //再执行关闭
                    });
                }else{
                    layer.alert(res.msg, {icon: 5});
                }
            },
            error: function(){
                layer.alert('操作失败，网络故障!', {icon: 5});
            }
        })
    })



});