layui.use(["table","jquery","layer"],function(){
    var table = layui.table;
    var $ = layui.jquery;
    var layer = layui.layer;


    //渲染数据表格
    function reload(){
        let keyWords = $("#keyWords").val();
        table.render({
            elem: "#dataTable"
            ,url: "/business/getRole?keyWords="+keyWords
            ,page: true
            ,cols : [[
                {field: "roleName", title: "角色名称", width:"30%"}
                ,{field: "roleDes", title: "角色描述", width:"30%"}
                ,{width:"40%", align:'center',title:'操作', toolbar: '#tool'}
            ]]
        });
    }


    //初始化渲染数据表格
    reload();

    table.on("tool(dataTable)",function (obj) {
        let layEvent = obj.event;
        let roleId = obj.data.roleId;
        //编辑角色
        if(layEvent === 'edit'){
            layer.open({
                type: 2,
                title: "编辑角色",
                shade: false,
                area: ["700px","650px"],
                content: "/business/updateRole?roleId="+roleId,
                end: function(){
                        reload();
                    }
            })
        //    删除角色
        }else if(layEvent === 'del'){
            $.ajax({
                type: "POST",
                url: "/business/deleteRole",
                data: {"roleId":roleId},
                success: function(res){
                    if(res.code===0){
                        layer.alert(res.msg, {icon: 6}, function () {
                            let index = layer.open(); //获取窗口索引
                            layer.close(index);
                            reload()
                        });
                    } else{
                        layer.alert(res.msg, {icon: 5});
                    }
                },
                error:function(){
                    layer.alert('操作失败，网络故障!', {icon: 5});
                }
            })
        }
    });


    //监听工具栏添加按钮
    $("#add").click(function () {
        layer.open({
            type: 2,
            shade: false,
            title: "添加角色",
            area: ["400px","300px"],
            content: "/business/addRole",
            end: function(){
                reload();
            }
        })
    });

    //搜索
    $("#search").click(function(){
        reload();
    });

    //刷新
    $("#refresh").click(function(){
        $("#keyWords").val("");
        reload();
        layer.msg("刷新成功！",{
            time: 1000
        })
    });

});