layui.use(["layer","jquery","form"],function () {
    var layer = layui.layer;
    var $ = layui.jquery;
    var form = layui.form;

    function reload(parentId){
        $.ajax({
            type: "GET",
            url: "/content/getCatalog?parentId=" + parentId,
            success: function(res){
                $("#value").html('<input type="hidden" name="parentId" value="'+parentId+'">');
                if(res.data.length===0){
                    $("#cataLogData").append('<div align="center">暂无数据</div>');
                }else{
                    for(i=0;i<res.data.length;i++){
                        let type = res.data[i].type;
                        let html = '<li type="'+type+'" class="layui-inline" style="padding: 20px 40px;" id="'+res.data[i].fileId+'">' +
                            '            <div style="text-align: center">' +
                            '                <img src="'+res.icon[type]+'" height="75" width="98.25" /><br>' +
                            '                <span>'+res.data[i].fileName+'</span>' +
                            '            </div>' +
                            '        </li>';
                        $("#cataLogData").append(html);
                    }
                }

            },
            error:function(){
                layer.alert('操作失败，网络故障!', {icon: 5});
            }
        })
    }

    reload(parentId=-1);


    $("ul.file").on("click","li",function(){
        let fileId = $(this).attr("id");
        let type = $(this).attr("type");
        let fileName = $(this).text();
        if(type==="0"){
            $("#cataLogData").html("");
            reload(parendtId=fileId);
        } else if(type==="1"){
            $.ajax({
                type: "POST",
                url: "/content/openCatalog",
                data: {"fileId":fileId},
                success: function(res){
                    let index = layer.open({
                        type:2,
                        title: fileName,
                        area: "auto",
                        content: res.url
                    });
                    layer.full(index);
                }
            });
        }else{
            $.ajax({
                type: "POST",
                url: "/content/openCatalog",
                data: {"fileId":fileId},
                success: function(res){
                    let index = layer.open({
                                    type:2,
                                    title: fileName,
                                    shade: false,
                                    area: "auto",
                                    content: res.src
                                });
                    layer.full(index);
                }
            });
        }

    });


    $("#goback").click(function(){
        let parent = $("input:hidden[name='parentId']").val();
        $("#cataLogData").html("");
        $.ajax({
            type: "POST",
            url: "/content/getCatalog",
            data: {"parentId": parent},
            success: function(res){
                $("#value").html('<input type="hidden" name="parentId" value="'+res.parent+'">');
                if(res.data.length===0){
                    $("#cataLogData").append('<div>暂无数据</div>');
                }else{
                   for(i=0;i<res.data.length;i++){
                        let type = res.data[i].type;
                        let html = '<li type="'+type+'" class="layui-inline" style="padding: 20px 40px;" id="'+res.data[i].fileId+'">' +
                            '            <div style="text-align: center">' +
                            '                <img src="'+res.icon[type]+'" height="75" width="98.25" /><br>' +
                            '                <span>'+res.data[i].fileName+'</span>' +
                            '            </div>' +
                            '        </li>';
                        $("#cataLogData").append(html);
                    }
                }

            },
            error:function(){
                layer.alert('操作失败，网络故障!', {icon: 5});
            }
        });
    });


    $("#add").click(function(){
        let parent = $("input:hidden[name='parentId']").val();
        layer.open({
            type: 2,
            title: "添加文件",
            shade: false,
            maxmin: true,
            area: ["700px","400px"],
            content: "/content/addFile?parentId=" + parent,
            end:function(){
                $("#cataLogData").html("");
                reload(parentId=parent);
            }
        })
    })

});