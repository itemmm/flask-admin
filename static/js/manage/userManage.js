layui.use(["table","jquery","layer"],function(){
    var table = layui.table;
    var $ = layui.jquery;
    var layer = layui.layer;


    function reload(){
        let keyWords = $("#keyWords").val();
        table.render({
            elem: "#dataTable"
            ,url: "/business/getUser?keyWords="+keyWords
            ,page: true
            ,cols : [[
                {field: "loginName", title: "账号", width:"30%"}
                ,{field: "nickName", title: "角色昵称", width:"30%"}
                ,{width:"40%", align:'center',title:'操作', toolbar: '#tool'}
            ]]
        });
    }


    //渲染数据表格
    reload();

    table.on("tool(dataTable)",function (obj) {
        let layEvent = obj.event;
        let userId = obj.data.userId;
        if(layEvent === 'edit'){
            layer.open({
                type: 2,
                title: "编辑用户",
                shade: false,
                area: ["700px","650px"],
                content: "/business/updateUser?userId="+userId,
                end:function(){
                        reload();
                    }
            })
        }else if(layEvent === 'del'){
            $.ajax({
                type: "POST",
                url: "/business/deleteUser",
                data: {"userId":userId},
                success: function(res){
                    if(res.code===0){
                        layer.alert(res.msg, {icon: 6}, function () {
                            let index = layer.open(); //获取窗口索引
                            layer.close(index);
                            reload();
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
            title: "添加用户",
            shade: false,
            area: ["700px","400px"],
            content: "/business/addUser",
            end:function(){
                reload();
            }
        })
    });

    $("#search").click(function () {
        reload();
    });

    $("#refresh").click(function(){
        $("#keyWords").val("");
        reload();
        layer.msg("刷新成功！",{
            time: 1000
        })
    })

});