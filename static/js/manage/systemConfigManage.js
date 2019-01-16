layui.use(["jquery","layer","table"],function(){
    var $ = layui.jquery;
    var layer = layui.layer;
    var table = layui.table;

    function reload(){
        table.render({
            elem: "#dataTable"
            ,url: "/business/getSystemConfig"
            ,cols : [[
                {field: "key", title: "参数名称", width:"20%"}
                ,{field: "value", title: "参数值", width:"20%"}
                ,{field: "des", title: "参数描述",width: "40%"}
                ,{width:"20%", align:'center',title:'操作', toolbar: '#tool'}
            ]]
        });
    }


    reload();

    table.on("tool(dataTable)",function (obj) {
        let layEvent = obj.event;
        let keyWordId = obj.data.keyWordId;
        if(layEvent === 'edit'){
            layer.open({
                type: 2,
                title: "编辑参数",
                shade: false,
                area: ["700px","450px"],
                content: "/business/updateSystemConfig?keyWordId="+keyWordId,
                end:function(){
                        reload();
                    }
            })
        }
    });

});