layui.use(["jquery","form","element"],function(){
    var $ = layui.jquery;
    var form = layui.form;
    var element = layui.element;


    $.ajax({
       type: "GET",
       url: "/business/menu",
       success: function(res){
           console.log(res);
           for(i=0;i<res.data.list.length;i++){
               let html_1 = '<div class="layui-colla-item">' +
                   '    <h2 class="layui-colla-title">'+res.data.list[i].name+'</h2>' +
                   '    <div class="layui-colla-content">';
               for(m=0;m<res.data.list[i].children.length;m++){
                   let html_2 = '<input type="checkbox" value="'+res.data.list[i].children[m].id+'" name="resource" title="'+res.data.list[i].children[m].name+'">'
                    html_1 = html_1 + html_2;
               }
               let html = html_1 + '  </div></div>';
               $("#resourceList").append(html);
           }
           element.render();
           form.render();
       }
    });


    form.on("submit(save)",function(data){
        let params = {"roleName":data.field.roleName,"roleDes":data.field.roleDes};
        $.ajax({
            type: "POST",
            url: "/business/addRole",
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